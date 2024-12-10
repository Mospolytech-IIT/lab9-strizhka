"""Модуль CRUD"""
from typing import List, Optional
from sqlalchemy.orm import Session
from models import User, Post

def create_user(session: Session, username: str, email: str, password: str) -> User:
    """Создание нового пользователя"""
    user = User(username=username, email=email, password=password)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def create_post(session: Session, title: str, content: str, user_id: int) -> Post:
    """Создание нового поста"""
    post = Post(title=title, content=content, user_id=user_id)
    session.add(post)
    session.commit()
    session.refresh(post)
    return post

def get_all_users(session: Session) -> List[User]:
    """Получение всех пользователей"""
    return session.query(User).all()

def get_all_posts(session: Session) -> List[Post]:
    """Получение всех постов"""
    return session.query(Post).all()

def get_posts_by_user(session: Session, user_id: int) -> List[Post]:
    """Получение постов конкретного пользователя"""
    return session.query(Post).filter(Post.user_id == user_id).all()

def update_user_email(session: Session, user_id: int, new_email: str) -> Optional[User]:
    """Обновить почту пользователя"""
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        user.email = new_email
        session.commit()
    return user

def update_post_content(session: Session, post_id: int, new_content: str) -> Optional[Post]:
    """Обновить пост"""
    post = session.query(Post).filter(Post.id == post_id).first()
    if post:
        post.content = new_content
        session.commit()
    return post

def delete_post(session: Session, post_id: int) -> None:
    """Удалить пост"""
    post = session.query(Post).filter(Post.id == post_id).first()
    if post:
        session.delete(post)
        session.commit()

def delete_user(session: Session, user_id: int) -> None:
    """Удалить пользователя и его посты"""
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        session.delete(user)
        session.commit()
