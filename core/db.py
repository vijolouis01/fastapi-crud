"""Database configuration and session management."""

from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from core import get_settings

settings = get_settings()


# Create engine with connection pooling
engine = create_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,  # Validate connection before using
    pool_recycle=3600,  # Recycle connections every hour
)

# Session factory
SessionLocal = sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency for getting database session.

    Yields:
        Session: SQLAlchemy database session

    Example:
        Used as a FastAPI dependency:
        @router.get("/")
        def get_items(db: Session = Depends(get_db)):
            return db.query(Item).all()
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
