from fastapi import APIRouter, HTTPException, Depends, status
from schemas.user import UserCreate
from db import get_db
from sqlalchemy.orm import Session
from typing import Annotated
from models.user import User

DBSession = Annotated[Session, Depends(get_db)]
router = APIRouter(tags=["Users"], prefix="/users")


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db:DBSession):
    create_user = User(**user.model_dump())
    db.add(create_user)
    db.commit()
    db.refresh(create_user)
    return create_user


@router.get("/", status_code=status.HTTP_200_OK)
def get_users(db:DBSession):
    users = db.query(User).all()
    return users


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
def get_user(user_id: int, db:DBSession):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found with this id"
        )
    return user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: DBSession):
    user = db.get(User, user_id)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found with this id",
        )

    db.delete(user)
    db.commit()

    return {"message": "User deleted successfully"}


@router.put("/{user_id}")
def update_user(user_id: int, user: UserCreate, db:DBSession):
    update_user=db.get(User, user_id)
    if update_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found with this id",
        )
    for key, value in user.model_dump().items():
        setattr(update_user, key, value)
    db.add(update_user)
    db.commit()
    db.refresh(update_user)
    return update_user    