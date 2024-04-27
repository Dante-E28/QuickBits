from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.config import settings


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

naming_convention = {
      "ix": "ix_%(column_0_label)s",
      "uq": "uq_%(table_name)s_%(column_0_name)s",
      "ck": "ck_%(table_name)s_%(constraint_name)s",
      "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
      "pk": "pk_%(table_name)s",
    }


# Базовый класс для моделей и миграций.
class Model(DeclarativeBase):
    metadata = MetaData(naming_convention=naming_convention)


async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)
