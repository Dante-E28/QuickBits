from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.config import settings
from src.constants import naming_convention


# Подключение к базе.
engine = create_async_engine(
    url=settings.DATABASE_url_asyncpg,
    echo=settings.DEBUG
)

new_session = async_sessionmaker(
    engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False
)


# Базовый класс для моделей и миграций.
class Model(DeclarativeBase):
    metadata = MetaData(naming_convention=naming_convention)


async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
