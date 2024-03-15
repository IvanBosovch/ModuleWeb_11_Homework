from typing import List
from datetime import datetime, date, timedelta
from sqlalchemy.orm import Session
from src.database.models import User, UserLogin
from src.schemas import UserBase, UserResponse, UserUpdate
from sqlalchemy import or_, and_, extract
from src.repository.login import get_user_by_email


async def get_users(db: Session, user_login: UserLogin,  info: str = None) -> List[User]:
    """
    Retrieves a list of users for a specific user with specified pagination parameters.

    :param info: Information about user. First name, last name or email.
    :type info: string or None
    :param user_login: The user to retrieve user for.
    :type user_login: UserLogin
    :param db: The database session.
    :type db: Session
    :return: A list of users.
    :rtype: List[User]
    """
    if info:
        return db.query(User).filter(and_(or_(User.first_name==info, User.last_name==info, User.email==info), User.user_id==user_login.id)).all()
    return db.query(User).filter(User.user_id==user_login.id).all()

async def get_user(user_id: int, user_login: UserLogin, db: Session) -> User:
    """
    Retrieves a single user with the specified ID for a specific user.

    :param user_id: The ID of the user to retrieve.
    :type user_id: int
    :param user_login: The user to retrieve the user for.
    :type user_login: UserLogin
    :param db: The database session.
    :type db: Session
    :return: The user with the specified ID, or None if it does not exist.
    :rtype: User | None
    """

    return db.query(User).filter(and_(User.id==user_id, User.user_id==user_login.id)).first()


async def create_user(body: UserBase, user_login: UserLogin, db: Session) -> User:
    """
    Creates a new user for a specific user.

    :param body: The data for the user to create.
    :type body: UserBase
    :param user_logn: The user to create the user for.
    :type user_login: UserLogin
    :param db: The database session.
    :type db: Session
    :return: The newly created user.
    :rtype: User
    """
    user = User(first_name=body.first_name, last_name=body.last_name,
                 email=body.email, phone=body.phone, birthday=body.birthday, data=body.data, user_id=user_login.id)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


async def update_user(user_id: int, body: UserUpdate, user_login: UserLogin, db: Session) -> User | None:
    """
    Updates a single user with the specified ID for a specific user.

    :param user_id: The ID of the user to update.
    :type user_id: int
    :param body: The updated data for the user.
    :type body: UserUpdate
    :param user_login: The user to update the user for.
    :type user_login: UserLogin
    :param db: The database session.
    :type db: Session
    :return: The updated user, or None if it does not exist.
    :rtype: User | None
    """
    user = db.query(User).filter(and_(User.user_id==user_login.id, User.id==user_id)).first()
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


async def remove_user(user_id: int, user_login: UserLogin, db: Session) -> User | None:
    """
    Removes a single user with the specified ID for a specific user.

    :param user_id: The ID of the user to remove.
    :type user_id: int
    :param user_login: The user to remove the user for.
    :type user_login: UserLogin
    :param db: The database session.
    :type db: Session
    :return: The removed user, or None if it does not exist.
    :rtype: User | None
    """
    user = db.query(User).filter(and_(User.user_id==user_login.id, User.id==user_id)).first()
    if user:
        db.delete(user)
        db.commit()
    return user


async def get_birthday(db: Session):
    """
    Retrieves a list of users, who have birthday during the week 

    :param db: The database session.
    :type db: Session
    :return: Retrieves a list of users or None
    :rtype: User | None
    """
    today = datetime.now().date()
    end_date = today + timedelta(days=7)
   

    result = (db.query(User).filter(or_(and_(extract("month", User.birthday) == today.month,
                                            extract("day", User.birthday) >= today.day,
                                            extract("day", User.birthday) <= end_date.day),
                                            and_(extract("month", User.birthday) == end_date.month,
                                            extract("day", User.birthday) <= end_date.day))).all())
    return result



