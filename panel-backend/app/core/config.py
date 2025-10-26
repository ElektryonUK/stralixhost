import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8100
    DATABASE_URL: str = "postgresql+asyncpg://user:pass@localhost:5432/stralix_panel"
    INTERNAL_CA_CERT: str | None = None
    AGENT_MTLS_ENABLED: bool = True
    JWT_SIGNING_KEY: str = "CHANGE_ME"

settings = Settings()
