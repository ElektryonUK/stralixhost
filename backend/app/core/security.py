from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import datetime, timezone
from typing import Optional

from app.db.database import get_db
from app.db.models import User, UserSession

bearer_scheme = HTTPBearer(auto_error=False)

async def get_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    if not credentials or credentials.scheme.lower() != 'bearer':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not authenticated')
    token = credentials.credentials
    # Validate session token and expiry
    session_obj = await db.scalar(
        select(UserSession).where(
            UserSession.session_token == token,
            UserSession.is_active == True,
            UserSession.expires_at > datetime.now(timezone.utc),
        )
    )
    if not session_obj:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid or expired session')
    # Touch last_accessed_at
    await db.execute(
        update(UserSession)
        .where(UserSession.id == session_obj.id)
        .values(last_accessed_at=datetime.now(timezone.utc))
    )
    user = await db.scalar(select(User).where(User.id == session_obj.user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='User not found')
    return user
