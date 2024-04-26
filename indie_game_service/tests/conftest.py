import asyncio
from typing import AsyncGenerator, Generator
import pytest
from httpx import AsyncClient
from src.database import Model
from tests.db import MockUnitOfWork, UOWDep_test, engine
from src.routers.likes_router import UOWDep
from src.config import settings
from src.main import app


app.dependency_overrides[UOWDep] = UOWDep_test


@pytest.fixture(autouse=True)
async def db():
    assert settings.MODE == 'TEST'
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)
        await conn.run_sync(Model.metadata.create_all)
    yield


@pytest.fixture(scope='session')
def even_loop(request) -> Generator:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as ac:
        yield ac


@pytest.fixture
def uow():
    return MockUnitOfWork()
