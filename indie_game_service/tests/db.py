from fastapi import Depends
from typing import Annotated
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.unitofwork import IUnitOfWork, UnitOfWork
from src.config import settings


engine = create_async_engine(
    url=settings.DATABASE_url_asyncpg,
    echo=True,
    poolclass=NullPool
)

new_session = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)


class MockUnitOfWork(UnitOfWork):
    def __init__(self) -> None:
        self.session_factory = new_session


UOWDep_test = Annotated[IUnitOfWork, Depends(MockUnitOfWork)]
