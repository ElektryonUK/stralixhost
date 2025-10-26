from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.security import get_current_user
from app.db.database import get_db
from app.db.models import User, UserRole, UserStatus, UserSession

class MeOut(BaseModel):
    id: str
    email: str
    role: UserRole
    first_name: str | None = None
    last_name: str | None = None
    email_verified: bool
    status: UserStatus

me = APIRouter(prefix="/auth", tags=["auth"])  # stays under /api/auth

@me.get('/me', response_model=MeOut)
async def auth_me(current_user: User = Depends(get_current_user)):
    return MeOut(
        id=str(current_user.id),
        email=current_user.email,
        role=current_user.role,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        email_verified=current_user.email_verified,
        status=current_user.status,
    )
