"""Модуль для инициализации бд"""
from models import Base
from database import engine

def main():
    """Функция для создания таблиц"""
    Base.metadata.create_all(engine)
    print("Таблицы пользователь и пост созданы")

if __name__ == "__main__":
    main()
