from pydantic import BaseModel, EmailStr, Field
from datetime import date
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
