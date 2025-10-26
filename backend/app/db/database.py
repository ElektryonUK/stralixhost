from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import __version__ as sqlalchemy_version
from app.core.config import settings
import logging
import asyncio

logger = logging.getLogger(__name__)

def ensure_asyncpg_url(database_url: str) -> str:
    """Ensure the database URL uses the asyncpg driver."""
    if database_url.startswith('postgresql+asyncpg://'):
        return database_url
    elif database_url.startswith('postgresql://'):
        # Convert standard postgresql:// to asyncpg version
        converted_url = database_url.replace('postgresql://', 'postgresql+asyncpg://', 1)
        logger.info(f"Converted DATABASE_URL to use asyncpg: {converted_url[:50]}...")
        return converted_url
    else:
        raise ValueError(f"Unsupported database URL scheme. Must start with postgresql:// or postgresql+asyncpg://. Got: {database_url[:20]}...")

# Ensure the URL uses asyncpg driver
database_url = ensure_asyncpg_url(settings.DATABASE_URL)
logger.info(f"Using SQLAlchemy {sqlalchemy_version} with asyncpg driver")

# Create single async engine with explicit async driver configuration
try:
    engine = create_async_engine(
        database_url,
        echo=False,
        future=True,
        poolclass=NullPool,  # Use NullPool for better async handling
        connect_args={
            "server_settings": {
                "application_name": "stralixhost_backend",
            },
            # Ensure asyncpg-specific settings
            "prepared_statement_cache_size": 100,
        }
    )
    logger.info("Async database engine created successfully")
except Exception as e:
    logger.error(f"Failed to create database engine: {e}")
    raise

# Create sessionmaker factory
SessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession
)

async def test_connection():
    """Test the database connection to ensure asyncpg is working."""
    try:
        async with engine.begin() as conn:
            result = await conn.execute("SELECT 1 as test")
            test_value = result.scalar()
            if test_value == 1:
                logger.info("Database connection test successful with asyncpg")
                return True
    except Exception as e:
        logger.error(f"Database connection test failed: {e}")
        return False
    return False

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

# Run connection test on module import (optional, can be removed in production)
if __name__ == "__main__":
    # This will only run if the module is executed directly
    asyncio.run(test_connection())
