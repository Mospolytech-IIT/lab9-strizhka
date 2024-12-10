"""Модуль для инициализации БД и запуска FastAPI"""
from typing import Optional
from backend.models import Base, Post, User
from backend.database import engine, SessionLocal
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from backend.crud import (
    create_user, create_post, get_all_users, get_all_posts,
    update_user_email, update_post_content, delete_post, delete_user
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class PostCreate(BaseModel):
    title: str
    content: str
    user_id: int

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

def get_db():
    """Зависимость для получения сессии базы данных"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/")
def add_user(user: UserCreate, db: Session = Depends(get_db)):
    """API эндпоинт для добавления пользователя"""
    return create_user(db, user.username, user.email, user.password)

@app.post("/posts/")
def add_post(post: PostCreate, db: Session = Depends(get_db)):
    """API эндпоинт для добавления поста"""
    return create_post(db, post.title, post.content, post.user_id)

@app.get("/users/")
def list_users(db: Session = Depends(get_db)):
    """API эндпоинт для вывода всех пользователей"""
    return get_all_users(db)

@app.get("/posts/")
def list_posts(db: Session = Depends(get_db)):
    """API эндпоинт для вывода всех постов"""
    return get_all_posts(db)

@app.put("/users/{user_id}")
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    """API эндпоинт для обновления пользователя"""
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.username:
        db_user.username = user.username
    if user.email:
        db_user.email = user.email
    if user.password:
        db_user.password = user.password
    db.commit()
    db.refresh(db_user)
    return db_user

@app.put("/posts/{post_id}")
def update_post(post_id: int, post: PostUpdate, db: Session = Depends(get_db)):
    """API эндпоинт для обновления поста"""
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.title:
        db_post.title = post.title
    if post.content:
        db_post.content = post.content
    db.commit()
    db.refresh(db_post)
    return db_post

@app.delete("/posts/{post_id}")
def remove_post(post_id: int, db: Session = Depends(get_db)):
    """API эндпоинт для удаления поста"""
    delete_post(db, post_id)
    return {"message": "Пост удален"}

@app.delete("/users/{user_id}")
def remove_user(user_id: int, db: Session = Depends(get_db)):
    """API эндпоинт для удаления пользователя"""
    delete_user(db, user_id)
    return {"message": "Пользователь и его посты удалены"}

@app.get("/")
def read_root():
    """Тестовый маршрут"""
    return {"message": "Сервер работает"}

@app.get("/initialize")
def initialize_db():
    """Маршрут для ручной инициализации таблиц"""
    Base.metadata.create_all(engine)
    return {"message": "Таблицы созданы"}

def main():
    """Функция для инициализации таблиц"""
    Base.metadata.create_all(engine)
    print("Таблицы пользователь и пост созданы")

if __name__ == "__main__":
    import uvicorn
    main()
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

