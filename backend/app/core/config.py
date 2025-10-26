import os
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost:5432/stralixhost"
    
    # Security
    SECRET_KEY: str = "CHANGE_ME_IN_PRODUCTION"
    
    # Tokens & Sessions
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    CORS_ORIGINS: str = "*"
    
    # App settings
    APP_NAME: str = "Stralix API"
    APP_ENV: str = "production"
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    
    # SMTP
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM_NAME: str = "Stralix"
    SMTP_TLS: bool = True
    
    # 2FA
    TOTP_ISSUER: str = "Stralix"
    
    # Cookies
    SESSION_COOKIE_NAME: str = "sx_s"
    REFRESH_COOKIE_NAME: str = "sx_r"
    COOKIE_DOMAIN: Optional[str] = None
    
    # Session binding
    BIND_SESSION_TO_IP: bool = True
    BIND_SESSION_TO_UA: bool = True
    
    # Rate limiting
    RATE_LIMIT_LOGIN_PER_MIN: int = 10
    RATE_LIMIT_VERIFY_PER_MIN: int = 10
    RATE_LIMIT_RESET_PER_MIN: int = 5
    
    # Logging
    LOG_LEVEL: str = "INFO"
    REQUEST_ID_HEADER: str = "X-Request-ID"
    
    # Feature flags
    ENABLE_EMAIL_VERIFICATION: bool = True
    ENABLE_2FA: bool = True
    
    # Optional admin bootstrap
    ADMIN_BOOTSTRAP_EMAIL: Optional[str] = None
    ADMIN_BOOTSTRAP_PASSWORD: Optional[str] = None
    
    @field_validator('DATABASE_URL')
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        if not v.startswith('postgresql+asyncpg://'):
            raise ValueError('DATABASE_URL must use postgresql+asyncpg:// scheme for async operations')
        return v

settings = Settings()
