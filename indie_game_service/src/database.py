from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import settings


# Подключение к базе.
engine = create_async_engine(
    url=settings.DATABASE_url_asyncpg,
    echo=settings.DEBUG
)


# Базовый класс для моделей и миграций.
class Base(DeclarativeBase):
    pass
