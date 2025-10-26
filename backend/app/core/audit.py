from __future__ import annotations
from datetime import datetime, timezone
from typing import Optional, Any

from sqlalchemy import String, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import SecurityAuditLog  # ensure this model exists; otherwise add migration

async def log_event(
    db: AsyncSession,
    *,
    user_id: Optional[str],
    action: str,
    ip: Optional[str] = None,
    ua: Optional[str] = None,
    meta: Optional[dict[str, Any]] = None,
) -> None:
    """Record a security/audit event.

    Expected actions include:
    - auth:login_success, auth:login_failure, auth:logout, auth:refresh
    - account:verify_email, account:forgot_password_request, account:reset_password
    - account:2fa_setup, account:2fa_verify
    """
    # If using ORM model
    if SecurityAuditLog is not None:
        entry = SecurityAuditLog(
            user_id=user_id,
            action=action,
            ip_address=ip,
            user_agent=ua,
            metadata_=meta or {},
            created_at=datetime.now(timezone.utc),
        )
        db.add(entry)
        await db.commit()
        return

    # Fallback raw SQL example (if model not present) - wrapped in text()
    await db.execute(
        text(
            """
            insert into security_audit_log (user_id, action, ip_address, user_agent, metadata, created_at)
            values (:user_id, :action, :ip, :ua, :meta::jsonb, :created_at)
            """
        ),
        {
            "user_id": user_id,
            "action": action,
            "ip": ip,
            "ua": ua,
            "meta": (meta or {}),
            "created_at": datetime.now(timezone.utc),
        },
    )
    await db.commit()
