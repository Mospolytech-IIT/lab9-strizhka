""""
Модуль для моделей данных
"""
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
    """Модель пользователя"""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")


class Post(Base):
    """Модель поста"""
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship("User", back_populates="posts")
