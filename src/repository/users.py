from typing import List
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
from src.database.models import User
from src.schemas import UserBase, UserResponse, UserUpdate
from sqlalchemy import or_, and_, extract


async def get_users(db: Session, info: str = None) -> List[User]:
    if info:
        return db.query(User).filter(or_(User.first_name==info, User.last_name==info, User.email==info)).all()
    return db.query(User).all()


async def get_user(user_id: int, db: Session) -> User:
    return db.query(User).filter(User.id==user_id).first()


async def create_user(body: UserBase, db: Session) -> User:
    user = User(first_name=body.first_name, last_name=body.last_name,
                 email=body.email, phone=body.phone, birthday=body.birthday, data=body.data)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


async def update_user(user_id: int, body: UserUpdate, db: Session) -> User | None:
    user = db.query(User).filter(User.id==user_id).first()
    if user:
        if body.first_name != 'string':
            user.first_name = body.first_name
        if body.last_name != 'string':
            user.last_name = body.last_name
        if body.email != 'user@example.com':
            user.email = body.email
        if body.phone != '+380964334566':
            user.phone = body.phone
        if body.birthday != datetime.today():
            user.birthday = body.birthday
        if body.data != 'string':
            user.data = body.data
        db.commit()
    return user


async def remove_user(user_id: int, db: Session) -> User | None:
    user = db.query(User).filter(User.id==user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user


async def get_birthday(db: Session):
    today = datetime.now().date()
    end_date = today + timedelta(days=7)
   

    result = (db.query(User).filter(or_(and_(extract("month", User.birthday) == today.month,
                                            extract("day", User.birthday) >= today.day,
                                            extract("day", User.birthday) <= end_date.day),
                                            and_(extract("month", User.birthday) == end_date.month,
                                            extract("day", User.birthday) <= end_date.day))).all())
    return result

