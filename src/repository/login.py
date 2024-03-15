from libgravatar import Gravatar
from sqlalchemy.orm import Session
from src.database.models import User
from src.database.models import UserLogin
from src.schemas import LoginModel


async def get_user_by_email(email: str, db: Session) -> UserLogin:
    '''
    Retrieves customer from email if it was create

    :param email: Email by which we are looking for a customer
    :type email: str
    :param db: The database session.
    :type db: Session
    :return: customer
    :rtype: UserLogin
    '''
    return db.query(UserLogin).filter(UserLogin.email == email).first()


async def create_user(body: LoginModel, db: Session) -> UserLogin:
    '''
    Create new customer for web site

    :param body: The data for the customer to create.
    :type body: LoginModel
    :param db: The database session.
    :type db: Session
    :return: The newly created customer
    :rtype: UserLogin
    '''
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = UserLogin(**body.model_dump(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)    
    return new_user


async def update_token(user: UserLogin, token: str | None, db: Session) -> None:
    """
    Update token for the specified user.

    :param user: The customer to update token for.
    :type user: UserLogin
    :param token: The refreshed token.
    :type token: str | None
    :param db: The database session.
    :type db: Session
    :return: None
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    '''
    Confirmed email for customer

    :param email: email by which we want confirmed
    :type email: str
    :param db: The database session.
    :type db: Session
    :return: None
    '''
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email: str, url: str, db: Session) -> UserLogin:
    '''
    Update avatar for customer

    :param email: Email customer's which avatar we want update 
    :type email: str
    :param url: url avatar
    :type url: str
    :param db: The database session.
    :type db: Session
    :return: info about customer
    :rtype: UserLogin
    '''
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user