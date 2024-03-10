from sqlalchemy import Column, Integer, String, func, Boolean
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(20))
    last_name = Column(String(20))
    email = Column(String(30))
    phone = Column(String(20))
    birthday = Column(DateTime)
    data = Column(String(50), nullable=True)
    user_id = Column('user_id', ForeignKey('users_login.id', ondelete='CASCADE'), default=None)
    user = relationship('UserLogin', backref="users")


class UserLogin(Base):
    __tablename__ = 'users_login'
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column('crated_at', DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)
