from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.database import create_table
from src.users.router import auth_router, user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_table()
    yield
    print('Конец приложения')

app = FastAPI(title='Юзер Сервис', lifespan=lifespan)


app.include_router(auth_router)
app.include_router(user_router)
