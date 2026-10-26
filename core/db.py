"""Database configuration and session management."""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from core.config import get_settings

settings = get_settings()


engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
    pool_recycle=3600,
    connect_args={
        "connect_timeout": 10,
        "server_settings": {"application_name": "fastapi-crud"},
    },
    max_overflow=10,
)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting async database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
