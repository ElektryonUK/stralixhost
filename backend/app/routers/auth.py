from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel, EmailStr, constr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from passlib.context import CryptContext
import secrets
import pyotp

from app.core.config import settings
from app.core.rate_limit import rate_limiter
from app.core.security import get_current_user_any
from app.core.audit import log_event
from app.core.email import send_verification_email
from app.db.database import get_db
from app.db.models import User, UserStatus, UserRole, UserSession

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

auth = APIRouter(prefix="/auth", tags=["auth"])

class RegisterIn(BaseModel):
  email: EmailStr
  password: constr(min_length=8)
  first_name: str | None = None
  last_name: str | None = None

class LoginIn(BaseModel):
  email: EmailStr
  password: str
  totp: str | None = None

class MeOut(BaseModel):
  id: str
  email: EmailStr
  role: UserRole
  first_name: str | None = None
  last_name: str | None = None
  email_verified: bool

@auth.post('/register', status_code=201)
async def register(payload: RegisterIn, request: Request, db: AsyncSession = Depends(get_db)):
  await rate_limiter.check(request, settings.RATE_LIMIT_LOGIN_PER_MIN)
  email = payload.email.lower().strip()
  exists = await db.scalar(select(User).where(User.email == email))
  if exists:
    raise HTTPException(status_code=400, detail='Email already registered')
  
  verification_token = secrets.token_urlsafe(32)
  user = User(
    email=email,
    password_hash=pwd_context.hash(payload.password),
    first_name=payload.first_name,
    last_name=payload.last_name,
    role=UserRole.customer,
    status=UserStatus.pending_verification,
    email_verified=False,
    email_verification_token=verification_token,
  )
  db.add(user)
  await db.commit()
  
  # Send verification email
  base_url = str(request.base_url).rstrip('/')
  await send_verification_email(user.email, verification_token, base_url)
  
  return { 'message': 'Registered. Please check your email to verify your account.' }

@auth.post('/login')
async def login(payload: LoginIn, request: Request, db: AsyncSession = Depends(get_db)):
  await rate_limiter.check(request, settings.RATE_LIMIT_LOGIN_PER_MIN)
  email = payload.email.lower().strip()
  user = await db.scalar(select(User).where(User.email == email))
  
  ip = request.client.host if request.client else None
  ua = request.headers.get('user-agent')
  
  if not user or not pwd_context.verify(payload.password, user.password_hash):
    # Log failed login attempt
    await log_event(db, user_id=str(user.id) if user else None, action='auth:login_failure', 
                   ip=ip, ua=ua, meta={'email': email, 'reason': 'invalid_credentials'})
    raise HTTPException(status_code=401, detail='Invalid credentials')
  
  if user.twofa_enabled:
    if not payload.totp:
      await log_event(db, user_id=str(user.id), action='auth:login_failure', 
                     ip=ip, ua=ua, meta={'email': email, 'reason': 'missing_totp'})
      raise HTTPException(status_code=400, detail='TOTP required')
    if not user.twofa_secret or not pyotp.TOTP(user.twofa_secret).verify(payload.totp, valid_window=1):
      await log_event(db, user_id=str(user.id), action='auth:login_failure', 
                     ip=ip, ua=ua, meta={'email': email, 'reason': 'invalid_totp'})
      raise HTTPException(status_code=401, detail='Invalid TOTP')
  
  from datetime import datetime, timedelta, timezone
  now = datetime.now(timezone.utc)
  session = UserSession(
    user_id=user.id,
    session_token=secrets.token_urlsafe(48),
    refresh_token=secrets.token_urlsafe(48),
    expires_at=now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    refresh_expires_at=now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    user_agent=ua,
    ip_address=ip,
  )
  db.add(session)
  user.last_login_at = now
  await db.commit()
  
  # Log successful login
  await log_event(db, user_id=str(user.id), action='auth:login_success', 
                 ip=ip, ua=ua, meta={'email': email, 'session_id': str(session.id)})
  
  return { 'access_token': session.session_token, 'refresh_token': session.refresh_token, 'token_type': 'bearer' }

@auth.post('/logout')
async def logout(request: Request, current: User = Depends(get_current_user_any), db: AsyncSession = Depends(get_db)):
  bearer = request.headers.get('authorization')
  cookie_token = request.cookies.get('sx_s')
  
  q = update(UserSession).where(UserSession.user_id == current.id)
  session_tokens = []
  
  if bearer and bearer.lower().startswith('bearer '):
    token = bearer.split(' ', 1)[1]
    q = q.where(UserSession.session_token == token)
    session_tokens.append(token)
  elif cookie_token:
    q = q.where(UserSession.session_token == cookie_token)
    session_tokens.append(cookie_token)
  else:
    # fallback: invalidate all active sessions
    q = q.where(UserSession.is_active == True)
  
  await db.execute(q.values(is_active=False))
  await db.commit()
  
  # Log logout
  ip = request.client.host if request.client else None
  ua = request.headers.get('user-agent')
  await log_event(db, user_id=str(current.id), action='auth:logout', 
                 ip=ip, ua=ua, meta={'session_tokens': session_tokens})
  
  return { 'message': 'Logged out' }

@auth.get('/me', response_model=MeOut)
async def me(current: User = Depends(get_current_user_any)):
  return MeOut(
    id=str(current.id),
    email=current.email,
    role=current.role,
    first_name=current.first_name,
    last_name=current.last_name,
    email_verified=current.email_verified,
  )