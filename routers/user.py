"""User API endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core import get_db
from models import User
from schemas import UserCreate, UserResponse

DBSession = Annotated[AsyncSession, Depends(get_db)]


router = APIRouter(tags=["Users"], prefix="/users")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def create_user(user: UserCreate, db: DBSession):
    """
    Create a new user.

    Args:
        user: User data to create
        db: Database session

    Returns:
        Created user with ID

    Raises:
        HTTPException: If email already exists
    """
    new_user = User(**user.model_dump())

    try:
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user
    except IntegrityError as err:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        ) from err


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[UserResponse])
async def get_users(
    db: DBSession,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum records to return"),
):
    """
    Get paginated list of all users.

    Args:
        db: Database session
        skip: Number of records to skip (default: 0)
        limit: Maximum records to return (default: 100, max: 1000)

    Returns:
        List of users
    """
    query = select(User).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user(user_id: int, db: DBSession):
    """
    Get a specific user by ID.

    Args:
        user_id: User ID
        db: Database session

    Returns:
        User object

    Raises:
        HTTPException: If user not found
    """
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found with this id",
        )
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: DBSession):
    """
    Delete a user by ID.

    Args:
        user_id: User ID
        db: Database session

    Raises:
        HTTPException: If user not found
    """
    user = await db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found with this id",
        )
    await db.delete(user)
    await db.commit()


@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user: UserCreate, db: DBSession):
    """
    Update a user by ID.

    Args:
        user_id: User ID
        user: Updated user data
        db: Database session

    Returns:
        Updated user object

    Raises:
        HTTPException: If user not found or email already exists
    """
    existing_user = await db.get(User, user_id)
    if existing_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found with this id",
        )

    for key, value in user.model_dump().items():
        setattr(existing_user, key, value)

    try:
        await db.commit()
        await db.refresh(existing_user)
        return existing_user
    except IntegrityError as err:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        ) from err
