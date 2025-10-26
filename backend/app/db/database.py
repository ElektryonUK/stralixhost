from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.core.config import settings

# Create single async engine - asyncpg driver is automatically detected from URL scheme
engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)

# Create sessionmaker factory
SessionLocal = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db():
    """Dependency to provide database session."""
    async with SessionLocal() as session:
        yield session
