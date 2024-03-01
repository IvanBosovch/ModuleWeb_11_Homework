from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime
from pydantic_extra_types.phone_numbers import PhoneNumber
from typing import Optional


class UserBase(BaseModel):
    first_name: str = Field(max_length=20)
    last_name: str = Field(max_length=20)
    email: EmailStr
    phone: Optional[PhoneNumber] = Field("+380964334566", max_length=20)
    birthday: date
    data: str = None

class UserUpdate(UserBase):
    pass


class UserResponse(UserBase):
    id: int
    email: EmailStr
    phone: PhoneNumber
    birthday: date
    data: str = None

    class Config:
        orm_mode = True


class LoginModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: str
    password: str = Field(min_length=6, max_length=10)


class LoginDb(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class LoginResponse(BaseModel):
    user: LoginDb
    detail: str = "User successfully created"


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"