from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel, EmailStr, constr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
import secrets
import pyotp

from app.core.config import settings
from app.core.rate_limit import rate_limiter
from app.core.security import get_current_user_any
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
  # Rate limit register similar to login
  await rate_limiter.check(request, settings.RATE_LIMIT_LOGIN_PER_MIN)
  email = payload.email.lower().strip()
  exists = await db.scalar(select(User).where(User.email == email))
  if exists:
    raise HTTPException(status_code=400, detail='Email already registered')
  user = User(
    email=email,
    password_hash=pwd_context.hash(payload.password),
    first_name=payload.first_name,
    last_name=payload.last_name,
    role=UserRole.customer,
    status=UserStatus.pending_verification,
    email_verified=False,
    email_verification_token=secrets.token_urlsafe(32),
  )
  db.add(user)
  await db.commit()
  return { 'message': 'Registered. Please verify your email.' }

@auth.post('/login')
async def login(payload: LoginIn, request: Request, db: AsyncSession = Depends(get_db)):
  await rate_limiter.check(request, settings.RATE_LIMIT_LOGIN_PER_MIN)
  email = payload.email.lower().strip()
  user = await db.scalar(select(User).where(User.email == email))
  if not user or not pwd_context.verify(payload.password, user.password_hash):
    raise HTTPException(status_code=401, detail='Invalid credentials')
  if user.twofa_enabled:
    if not payload.totp:
      raise HTTPException(status_code=400, detail='TOTP required')
    if not user.twofa_secret or not pyotp.TOTP(user.twofa_secret).verify(payload.totp, valid_window=1):
      raise HTTPException(status_code=401, detail='Invalid TOTP')
  from datetime import datetime, timedelta, timezone
  now = datetime.now(timezone.utc)
  session = UserSession(
    user_id=user.id,
    session_token=secrets.token_urlsafe(48),
    refresh_token=secrets.token_urlsafe(48),
    expires_at=now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    refresh_expires_at=now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
    user_agent=request.headers.get('user-agent'),
    ip_address=request.client.host if request.client else None,
  )
  db.add(session)
  user.last_login_at = now
  await db.commit()
  return { 'access_token': session.session_token, 'refresh_token': session.refresh_token, 'token_type': 'bearer' }

@auth.post('/logout')
async def logout(request: Request, current: User = Depends(get_current_user_any), db: AsyncSession = Depends(get_db)):
  # Invalidate session by either Authorization bearer or cookie token
  bearer = request.headers.get('authorization')
  cookie_token = request.cookies.get('sx_s')
  from sqlalchemy import update
  q = update(UserSession).where(UserSession.user_id == current.id)
  if bearer and bearer.lower().startswith('bearer '):
    token = bearer.split(' ', 1)[1]
    q = q.where(UserSession.session_token == token)
  elif cookie_token:
    q = q.where(UserSession.session_token == cookie_token)
  else:
    # fallback: invalidate all active sessions of current user
    q = q.where(UserSession.is_active == True)
  await db.execute(q.values(is_active=False))
  await db.commit()
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
