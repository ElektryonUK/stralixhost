from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import datetime, timezone
from typing import Optional

from app.db.database import get_db
from app.db.models import User, UserSession

bearer_scheme = HTTPBearer(auto_error=False)

async def _resolve_user_by_session(db: AsyncSession, token: str) -> Optional[User]:
    session_obj = await db.scalar(
        select(UserSession).where(
            UserSession.session_token == token,
            UserSession.is_active == True,
            UserSession.expires_at > datetime.now(timezone.utc),
        )
    )
    if not session_obj:
        return None
    await db.execute(
        update(UserSession)
        .where(UserSession.id == session_obj.id)
        .values(last_accessed_at=datetime.now(timezone.utc))
    )
    user = await db.scalar(select(User).where(User.id == session_obj.user_id))
    return user

async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    if not credentials or credentials.scheme.lower() != 'bearer':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authenticated')
    user = await _resolve_user_by_session(db, credentials.credentials)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid or expired session')
    return user

async def get_current_user_cookie(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> User:
    token = request.cookies.get('sx_s')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authenticated')
    user = await _resolve_user_by_session(db, token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid or expired session')
    return user

async def get_current_user_any(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    # Try bearer first
    if credentials and credentials.scheme.lower() == 'bearer':
        user = await _resolve_user_by_session(db, credentials.credentials)
        if user:
            return user
    # Fallback to cookie
    token = request.cookies.get('sx_s')
    if token:
        user = await _resolve_user_by_session(db, token)
        if user:
            return user
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authenticated')
