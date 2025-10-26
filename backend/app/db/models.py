from datetime import datetime, timezone
from sqlalchemy import Enum, String, Boolean, DateTime, text, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID, INET, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
import enum
import uuid

class UserRole(str, enum.Enum):
    customer = "customer"
    staff = "staff"
    admin = "admin"

class UserStatus(str, enum.Enum):
    active = "active"
    suspended = "suspended"
    banned = "banned"
    pending_verification = "pending_verification"

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(50), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))

    first_name: Mapped[str | None] = mapped_column(String(100))
    last_name: Mapped[str | None] = mapped_column(String(100))
    phone_number: Mapped[str | None] = mapped_column(String(20))
    avatar_url: Mapped[str | None] = mapped_column(String)

    role: Mapped[UserRole] = mapped_column(Enum(UserRole, name="user_role"), default=UserRole.customer)
    status: Mapped[UserStatus] = mapped_column(Enum(UserStatus, name="user_status"), default=UserStatus.pending_verification)

    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    email_verification_token: Mapped[str | None] = mapped_column(String(255))
    email_verification_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    reset_password_token: Mapped[str | None] = mapped_column(String(255))
    reset_password_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    twofa_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    twofa_secret: Mapped[str | None] = mapped_column(String(255))
    twofa_backup_codes: Mapped[list[str] | None] = mapped_column(ARRAY(String))

    last_login_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    last_login_ip: Mapped[str | None] = mapped_column(INET)
    failed_login_attempts: Mapped[int] = mapped_column(default=0)
    locked_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=text("CURRENT_TIMESTAMP"), onupdate=datetime.now(timezone.utc))

class UserSession(Base):
    __tablename__ = "user_sessions"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    session_token: Mapped[str] = mapped_column(String(255), unique=True)
    refresh_token: Mapped[str | None] = mapped_column(String(255), unique=True)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    refresh_expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    user_agent: Mapped[str | None] = mapped_column(String)
    ip_address: Mapped[str | None] = mapped_column(INET)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    last_accessed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class SecurityAuditLog(Base):
    __tablename__ = "security_audit_log"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"))
    event_type: Mapped[str] = mapped_column(String(50))
    event_description: Mapped[str | None] = mapped_column(String)
    ip_address: Mapped[str | None] = mapped_column(INET)
    user_agent: Mapped[str | None] = mapped_column(String)
    request_id: Mapped[str | None] = mapped_column(String(100))
    metadata: Mapped[dict | None] = mapped_column(JSON)
    severity: Mapped[str] = mapped_column(String(20), default="info")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
