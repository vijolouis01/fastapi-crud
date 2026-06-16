from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from core import get_db
from models import User
from schemas import UserCreate, UserResponse

DBSession = Annotated[Session, Depends(get_db)]


router = APIRouter(tags=["Users"], prefix="/users")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: DBSession):
    new_user = User(**user.model_dump())

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError as err:
        db.rollback()
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Email already exists",
    ) from err


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[UserResponse])
def get_users(db: DBSession):
    return db.query(User).all()


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
def get_user(user_id: int, db: DBSession):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found with this id"
        )
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: DBSession):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found with this id",
        )
    db.delete(user)
    db.commit()


@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_user(user_id: int, user: UserCreate, db: DBSession):
    existing_user = db.get(User, user_id)
    if existing_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found with this id",
        )
    for key, value in user.model_dump().items():
        setattr(existing_user, key, value)
    try:
        db.commit()
        db.refresh(existing_user)
        return existing_user
    except IntegrityError as err:
        db.rollback()
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Email already exists",
    ) from err
