from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, EmailStr, constr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import datetime, timedelta, timezone
import secrets
from passlib.context import CryptContext
import pyotp

from app.core.config import settings
from app.core.security import get_current_user
from app.core.rate_limit import rate_limiter
from app.core.audit import log_event
from app.core.email import send_password_reset_email
from app.db.database import get_db
from app.db.models import User, UserSession, UserStatus

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

account = APIRouter(prefix="/account", tags=["account"])

# Schemas
class ForgotPasswordIn(BaseModel):
    email: EmailStr

class ResetPasswordIn(BaseModel):
    token: str
    new_password: constr(min_length=8)

class VerifyEmailIn(BaseModel):
    token: str

class Setup2FAOut(BaseModel):
    secret: str
    otpauth_url: str

class Verify2FAIn(BaseModel):
    code: constr(min_length=6, max_length=6)

@account.post('/verify-email')
async def verify_email(payload: VerifyEmailIn, request: Request, db: AsyncSession = Depends(get_db)):
    await rate_limiter.check(request, settings.RATE_LIMIT_VERIFY_PER_MIN)
    user = await db.scalar(select(User).where(User.email_verification_token == payload.token))
    if not user:
        raise HTTPException(status_code=400, detail='Invalid token')
    user.email_verified = True
    user.status = UserStatus.active
    user.email_verification_token = None
    await db.commit()
    await log_event(db, user_id=str(user.id), action='account:verify_email', 
                   ip=request.client.host if request.client else None, 
                   ua=request.headers.get('user-agent'))
    return { 'message': 'Email verified' }

@account.post('/forgot-password')
async def forgot_password(payload: ForgotPasswordIn, request: Request, db: AsyncSession = Depends(get_db)):
    await rate_limiter.check(request, settings.RATE_LIMIT_VERIFY_PER_MIN)
    email = payload.email.lower().strip()
    user = await db.scalar(select(User).where(User.email == email))
    
    if user:
        user.reset_password_token = secrets.token_urlsafe(32)
        user.reset_password_expires_at = datetime.now(timezone.utc) + timedelta(hours=1)
        await db.commit()
        
        # Send password reset email using centralized utility
        base_url = str(request.base_url).rstrip('/')
        await send_password_reset_email(user.email, user.reset_password_token, base_url)
        
        await log_event(db, user_id=str(user.id), action='account:forgot_password_request', 
                       ip=request.client.host if request.client else None, 
                       ua=request.headers.get('user-agent'))
    
    return { 'message': 'If the email exists, a reset link has been sent.' }

@account.post('/reset-password')
async def reset_password(payload: ResetPasswordIn, request: Request, db: AsyncSession = Depends(get_db)):
    await rate_limiter.check(request, settings.RATE_LIMIT_RESET_PER_MIN)
    user = await db.scalar(select(User).where(User.reset_password_token == payload.token))
    if not user or not user.reset_password_expires_at or user.reset_password_expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail='Invalid or expired token')
    
    user.password_hash = pwd_context.hash(payload.new_password)
    user.reset_password_token = None
    user.reset_password_expires_at = None
    
    # Invalidate all active sessions for security
    await db.execute(update(UserSession).where(UserSession.user_id == user.id).values(is_active=False))
    await db.commit()
    
    await log_event(db, user_id=str(user.id), action='account:reset_password', 
                   ip=request.client.host if request.client else None, 
                   ua=request.headers.get('user-agent'))
    
    return { 'message': 'Password has been reset' }

@account.post('/2fa/setup', response_model=Setup2FAOut)
async def setup_2fa(request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    secret = pyotp.random_base32()
    otpauth_url = pyotp.totp.TOTP(secret).provisioning_uri(name=current_user.email, issuer_name=settings.TOTP_ISSUER)
    current_user.twofa_secret = secret
    await db.commit()
    
    await log_event(db, user_id=str(current_user.id), action='account:2fa_setup', 
                   ip=request.client.host if request.client else None, 
                   ua=request.headers.get('user-agent'))
    
    return Setup2FAOut(secret=secret, otpauth_url=otpauth_url)

@account.post('/2fa/verify')
async def verify_2fa(payload: Verify2FAIn, request: Request, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if not current_user.twofa_secret:
        raise HTTPException(status_code=400, detail='2FA not initialized')
    
    totp = pyotp.TOTP(current_user.twofa_secret)
    if not totp.verify(payload.code, valid_window=1):
        raise HTTPException(status_code=400, detail='Invalid code')
    
    current_user.twofa_enabled = True
    await db.commit()
    
    await log_event(db, user_id=str(current_user.id), action='account:2fa_verify', 
                   ip=request.client.host if request.client else None, 
                   ua=request.headers.get('user-agent'))
    
    return { 'message': '2FA enabled' }