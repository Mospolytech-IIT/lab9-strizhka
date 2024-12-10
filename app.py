"""Модуль FastAPI"""
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from crud import (
    create_user, create_post, get_all_users, get_all_posts,
    update_user_email, update_post_content, delete_post, delete_user
)

app = FastAPI()

def get_db():
    """Зависимость для получения сессии базы данных"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/users/")
def add_user(username: str, email: str, password: str, db: Session = Depends(get_db)):
    """API эндпоинт для добавления пользователя"""
    return create_user(db, username, email, password)

@app.post("/posts/")
def add_post(title: str, content: str, user_id: int, db: Session = Depends(get_db)):
    """API эндпоинт для добавления поста"""
    return create_post(db, title, content, user_id)

@app.get("/users/")
def list_users(db: Session = Depends(get_db)):
    """API эндпоинт для вывода всех пользователей"""
    return get_all_users(db)

@app.get("/posts/")
def list_posts(db: Session = Depends(get_db)):
    """API эндпоинт для вывода всех постов"""
    return get_all_posts(db)

@app.put("/users/{user_id}/email")
def change_user_email(user_id: int, new_email: str, db: Session = Depends(get_db)):
    """API эндпоинт для обновления почты"""
    return update_user_email(db, user_id, new_email)

@app.put("/posts/{post_id}/content")
def change_post_content(post_id: int, new_content: str, db: Session = Depends(get_db)):
    """API эндпоинт для обновления поста"""
    return update_post_content(db, post_id, new_content)

@app.delete("/posts/{post_id}")
def remove_post(post_id: int, db: Session = Depends(get_db)):
    """API эндпоинт для удаления поста"""
    delete_post(db, post_id)
    return {"message": "Пост удален "}

@app.delete("/users/{user_id}")
def remove_user(user_id: int, db: Session = Depends(get_db)):
    """API эндпоинт для удаления пользователя"""
    delete_user(db, user_id)
    return {"message": "Пользователь и его посты удалены"}
