from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Ensure the URL uses asyncpg driver
database_url = settings.DATABASE_URL
if not database_url.startswith('postgresql+asyncpg://'):
    logger.warning(f"DATABASE_URL does not use asyncpg driver: {database_url}")
    # Convert postgresql:// to postgresql+asyncpg://
    if database_url.startswith('postgresql://'):
        database_url = database_url.replace('postgresql://', 'postgresql+asyncpg://', 1)
        logger.info(f"Converted DATABASE_URL to use asyncpg: {database_url}")

# Create single async engine with explicit async driver configuration
engine = create_async_engine(
    database_url,
    echo=False,
    future=True,
    poolclass=NullPool,  # Use NullPool for better async handling
    connect_args={
        "server_settings": {
            "application_name": "stralixhost_backend",
        }
    }
)

# Create sessionmaker factory
SessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)

async def get_db():
    """Dependency to provide database session."""
    async with SessionLocal() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()
