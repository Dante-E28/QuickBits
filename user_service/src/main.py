from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.database import create_table


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_table()
    yield
    print('Конец приложения')

app = FastAPI(title='Инди Сервис', lifespan=lifespan)
