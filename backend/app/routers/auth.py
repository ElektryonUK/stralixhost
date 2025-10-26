from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel, EmailStr, constr
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import select
from passlib.context import CryptContext
import secrets
import pyotp

from app.core.config import settings
from app.db.models import User, UserStatus, UserRole, UserSession

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create async engine - asyncpg driver is automatically detected from URL scheme
engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

auth = APIRouter(prefix="/auth", tags=["auth"])

# Schemas
class RegisterIn(BaseModel):
  email: EmailStr
  password: constr(min_length=8)
  first_name: Optional[str] = None
  last_name: Optional[str] = None

class LoginIn(BaseModel):
  email: EmailStr
  password: str
  totp: Optional[str] = None

class MeOut(BaseModel):
  id: str
  email: EmailStr
  role: UserRole
  first_name: Optional[str] = None
  last_name: Optional[str] = None
  email_verified: bool

async def get_db():
  async with SessionLocal() as session:
    yield session

# Helpers
def hash_password(password: str) -> str:
  return pwd_context.hash(password)

def verify_password(password: str, password_hash: str) -> bool:
  return pwd_context.verify(password, password_hash)

# Routes
@auth.post('/register', status_code=201)
async def register(payload: RegisterIn, request: Request, db: AsyncSession = Depends(get_db)):
  # Normalize
  email = payload.email.lower().strip()
  # Ensure unique
  exists = await db.scalar(select(User).where(User.email == email))
  if exists:
    raise HTTPException(status_code=400, detail='Email already registered')
  # Create user
  user = User(
    email=email,
    password_hash=hash_password(payload.password),
    first_name=payload.first_name,
    last_name=payload.last_name,
    role=UserRole.customer,
    status=UserStatus.pending_verification,
    email_verified=False,
    email_verification_token=secrets.token_urlsafe(32),
  )
  db.add(user)
  await db.commit()
  # TODO: send verification email with token
  return { 'message': 'Registered. Please verify your email.' }

@auth.post('/login')
async def login(payload: LoginIn, request: Request, db: AsyncSession = Depends(get_db)):
  email = payload.email.lower().strip()
  user = await db.scalar(select(User).where(User.email == email))
  if not user or not verify_password(payload.password, user.password_hash):
    raise HTTPException(status_code=401, detail='Invalid credentials')
  # 2FA check
  if user.twofa_enabled:
    if not payload.totp:
      raise HTTPException(status_code=400, detail='TOTP required')
    if not user.twofa_secret or not pyotp.TOTP(user.twofa_secret).verify(payload.totp, valid_window=1):
      raise HTTPException(status_code=401, detail='Invalid TOTP')
  # Create session
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
async def logout(request: Request, db: AsyncSession = Depends(get_db)):
  # Invalidate by token from Authorization header or cookie (implementation detail TBD)
  return { 'message': 'Logged out' }

@auth.get('/me', response_model=MeOut)
async def me(db: AsyncSession = Depends(get_db)):
  # Placeholder: fetch user from session (to be implemented)
  raise HTTPException(status_code=401, detail='Not authenticated')
