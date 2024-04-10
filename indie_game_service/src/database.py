from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.config import settings
from sqlalchemy.ext.asyncio import async_sessionmaker


# Подключение к базе.
engine = create_async_engine(
    url=settings.DATABASE_url_asyncpg,
    echo=settings.DEBUG
)

new_session = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Базовый класс для моделей и миграций.
class Model(DeclarativeBase):
    pass


async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
