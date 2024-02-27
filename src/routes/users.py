from typing import List
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import UserBase, UserResponse, UserUpdate
from src.repository import users as repository_users

router = APIRouter(prefix='/users', tags=["users"])
router_birth = APIRouter(prefix='/users/birthdays', tags=['users'])


@router.get("/", response_model=List[UserResponse])
async def get_users(db: Session = Depends(get_db), info: str = None):
    users = await repository_users.get_users(db, info)
    return users


@router.get('/{user_id}', response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = await repository_users.get_user(user_id, db)
    if user is None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.post('/', response_model=UserResponse)
async def create_user(body: UserBase, db: Session = Depends(get_db)):
    return await repository_users.create_user(body, db)


@router.put('/{user_id}', response_model=UserResponse)
async def update_user(user_id: int, body: UserUpdate, db: Session = Depends(get_db)):
    user = await repository_users.update_user(user_id, body, db)
    if user is None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.delete('/{user_id}', response_model=UserResponse)
async def remove_user(user_id: int, db: Session = Depends(get_db)):
    user = await repository_users.remove_user(user_id, db)
    if user is None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

    
@router_birth.get('/', response_model=List[UserResponse])
async def get_birthday(db: Session = Depends(get_db)):
    birthday = await repository_users.get_birthday(db)
    if birthday is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Birthdays not found")
    return birthday