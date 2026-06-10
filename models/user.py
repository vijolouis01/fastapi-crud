"""User database model using SQLAlchemy ORM."""

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all ORM models."""

    pass


class User(Base):
    """
    User database model.

    Attributes:
        id: Primary key, auto-incremented integer
        name: User's full name
        email: User's email address
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str]
    email: Mapped[str] = mapped_column(index=True, unique=True)

    def __repr__(self) -> str:
        """Return string representation of User."""
        return f"<User(id={self.id}, name={self.name}, email={self.email})>"
