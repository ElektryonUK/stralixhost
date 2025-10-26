from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.core.security import get_current_user
from app.db.models import User, UserRole, UserStatus

me_router = APIRouter(prefix="/users", tags=["users"])

class MeOut(BaseModel):
    id: str
    email: str
    role: UserRole
    first_name: str | None = None
    last_name: str | None = None
    email_verified: bool
    status: UserStatus

@me_router.get('/me', response_model=MeOut)
async def get_me(current_user: User = Depends(get_current_user)):
    return MeOut(
        id=str(current_user.id),
        email=current_user.email,
        role=current_user.role,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        email_verified=current_user.email_verified,
        status=current_user.status,
    )
