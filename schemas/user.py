"""Pydantic schemas for user requests and responses."""

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """
    Schema for creating a new user.

    Attributes:
        name: User's full name (1-100 characters)
        email: User's email address
    """

    name: str = Field(..., min_length=1, max_length=100, description="User's full name")
    email: EmailStr = Field(..., description="User's email address")


class UserResponse(BaseModel):
    """
    Schema for user API responses.

    Attributes:
        id: User's unique identifier
        name: User's full name
        email: User's email address
    """

    id: int = Field(..., description="User's unique identifier")
    name: str = Field(..., description="User's full name")
    email: EmailStr = Field(..., description="User's email address")

    model_config = {"from_attributes": True}
