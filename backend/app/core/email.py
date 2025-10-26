import asyncio
import smtplib
from email.message import EmailMessage
from typing import Optional

from app.core.config import settings


async def send_email_async(
    to: str,
    subject: str,
    body: str,
    *,
    from_name: Optional[str] = None,
    from_email: Optional[str] = None,
) -> None:
    """Send an email asynchronously using SMTP settings."""
    if not settings.SMTP_HOST or not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        # Skip sending in development if SMTP not configured
        return
    
    msg = EmailMessage()
    sender_name = from_name or settings.SMTP_FROM_NAME
    sender_email = from_email or settings.SMTP_USER
    msg["From"] = f"{sender_name} <{sender_email}>"
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)
    
    # Run SMTP in thread to avoid blocking
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, _send_email_sync, msg)


def _send_email_sync(msg: EmailMessage) -> None:
    """Synchronous SMTP sending helper."""
    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as s:
        if settings.SMTP_TLS:
            s.starttls()
        s.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
        s.send_message(msg)


async def send_verification_email(
    to: str,
    token: str,
    base_url: str,
) -> None:
    """Send email verification email with token link."""
    verify_url = f"{base_url}/verify-email?token={token}"
    subject = f"Verify your {settings.TOTP_ISSUER} account"
    body = f"""Hello,

Please verify your email address by clicking the link below:

{verify_url}

This link will expire in 24 hours.

If you didn't create an account with {settings.TOTP_ISSUER}, please ignore this email.

Best regards,
The {settings.TOTP_ISSUER} Team
"""
    await send_email_async(to, subject, body)


async def send_password_reset_email(
    to: str,
    token: str,
    base_url: str,
) -> None:
    """Send password reset email with token link."""
    reset_url = f"{base_url}/reset-password?token={token}"
    subject = f"Reset your {settings.TOTP_ISSUER} password"
    body = f"""Hello,

You requested a password reset for your {settings.TOTP_ISSUER} account.

Click the link below to reset your password:

{reset_url}

This link will expire in 1 hour.

If you didn't request a password reset, please ignore this email and your password will remain unchanged.

Best regards,
The {settings.TOTP_ISSUER} Team
"""
    await send_email_async(to, subject, body)