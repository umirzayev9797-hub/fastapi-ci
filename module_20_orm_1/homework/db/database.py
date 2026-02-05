from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Используем SQLite. БД будет создана в корне проекта.
DATABASE_URL = "sqlite:///./library.db"

# engine — «двигатель», который общается с файлом БД
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}, # Нужно только для SQLite
    echo=False # Поставь True, если препод захочет увидеть SQL в консоли
)

# SessionLocal — класс для создания сессий (транзакций)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для всех моделей
Base = declarative_base()