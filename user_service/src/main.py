from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.rabbitmq.server import RabbitServer
from src.users.router import auth_router, user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    rabbit_server = await RabbitServer.create_server()
    yield
    await rabbit_server.close_connection()


app = FastAPI(title='Юзер Сервис', lifespan=lifespan)

app.include_router(auth_router)
app.include_router(user_router)
