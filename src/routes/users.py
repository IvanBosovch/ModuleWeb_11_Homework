from typing import List
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from src.database.models import UserLogin
from src.database.db import get_db
from src.schemas import UserBase, UserResponse, UserUpdate
from src.repository import users as repository_users
from src.services.auth import auth_service


router = APIRouter(prefix='/users', tags=["users"])
router_birth = APIRouter(prefix='/users/birthdays', tags=['users'])


@router.get("/", response_model=List[UserResponse])
async def get_users(db: Session = Depends(get_db), current_user: UserLogin = Depends(auth_service.get_current_user), info: str = None):
    users = await repository_users.get_users(db, current_user, info)
    return users


@router.get('/{user_id}', response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db), current_user: UserLogin = Depends(auth_service.get_current_user)):
    user = await repository_users.get_user(user_id, current_user, db)
    if user is None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.post('/', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(body: UserBase, db: Session = Depends(get_db), current_user: UserLogin = Depends(auth_service.get_current_user)):
    return await repository_users.create_user(body, current_user, db)


@router.put('/{user_id}', response_model=UserResponse)
async def update_user(user_id: int, body: UserUpdate, db: Session = Depends(get_db), current_user: UserLogin = Depends(auth_service.get_current_user)):
    user = await repository_users.update_user(user_id, body, current_user, db)
    if user is None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.delete('/{user_id}', response_model=UserResponse)
async def remove_user(user_id: int, db: Session = Depends(get_db), current_user: UserLogin = Depends(auth_service.get_current_user)):
    user = await repository_users.remove_user(user_id, current_user, db)
    if user is None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

    
@router_birth.get('/', response_model=List[UserResponse])
async def get_birthday(db: Session = Depends(get_db)):
    birthday = await repository_users.get_birthday(db)
    if birthday is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Birthdays not found")
    return birthday