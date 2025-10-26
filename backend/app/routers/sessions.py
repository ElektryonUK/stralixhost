from fastapi import APIRouter, Depends, HTTPException, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import datetime, timedelta, timezone
import secrets

from app.core.config import settings
from app.core.security import get_db
from app.db.models import UserSession

COOKIE_SESSION = "sx_s"
COOKIE_REFRESH = "sx_r"
COOKIE_DOMAIN = None  # set from env in production

sessions = APIRouter(prefix="/auth", tags=["auth-cookies"])

# Helpers

def set_auth_cookies(response: Response, session_token: str, refresh_token: str):
    domain = COOKIE_DOMAIN
    response.set_cookie(
        key=COOKIE_SESSION,
        value=session_token,
        httponly=True,
        secure=True,
        samesite="lax",
        path="/",
        domain=domain,
        max_age=int(timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES).total_seconds()),
    )
    response.set_cookie(
        key=COOKIE_REFRESH,
        value=refresh_token,
        httponly=True,
        secure=True,
        samesite="strict",
        path="/api/auth",
        domain=domain,
        max_age=int(timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS).total_seconds()),
    )

def clear_auth_cookies(response: Response):
    domain = COOKIE_DOMAIN
    for key, path in [(COOKIE_SESSION, "/"), (COOKIE_REFRESH, "/api/auth")]:
        response.delete_cookie(key=key, path=path, domain=domain)

@sessions.post('/refresh')
async def refresh(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    refresh_cookie = request.cookies.get(COOKIE_REFRESH)
    if not refresh_cookie:
        raise HTTPException(status_code=401, detail='No refresh token')
    now = datetime.now(timezone.utc)
    session_obj = await db.scalar(
        select(UserSession).where(
            UserSession.refresh_token == refresh_cookie,
            UserSession.is_active == True,
            UserSession.refresh_expires_at > now,
        )
    )
    if not session_obj:
        raise HTTPException(status_code=401, detail='Invalid refresh')
    # Rotate
    new_session = secrets.token_urlsafe(48)
    new_refresh = secrets.token_urlsafe(48)
    await db.execute(
        update(UserSession)
        .where(UserSession.id == session_obj.id)
        .values(
            session_token=new_session,
            refresh_token=new_refresh,
            expires_at=now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            refresh_expires_at=now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        )
    )
    await db.commit()
    set_auth_cookies(response, new_session, new_refresh)
    return { 'message': 'refreshed' }

@sessions.post('/logout')
async def logout(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    sess = request.cookies.get(COOKIE_SESSION)
    ref = request.cookies.get(COOKIE_REFRESH)
    if sess or ref:
        await db.execute(
            update(UserSession)
            .where((UserSession.session_token == sess) | (UserSession.refresh_token == ref))
            .values(is_active=False)
        )
        await db.commit()
    clear_auth_cookies(response)
    return { 'message': 'logged out' }
