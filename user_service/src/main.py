from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.database import create_table
from src.router import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_table()
    yield
    print('Конец приложения')

app = FastAPI(title='Юзер Сервис', lifespan=lifespan)


app.include_router(users_router, prefix='/users', tags=['Users'])
