from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.users.router import auth_router, user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title='Юзер Сервис', lifespan=lifespan)


app.include_router(auth_router)
app.include_router(user_router)
