from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.rabbitmq.client import rabbit_connection, rabbit_client
from src.routers.comments_router import router as comments_router
from src.routers.likes_router import router as likes_router
from src.routers.posts_router import router as posts_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await rabbit_connection.connect()
    rabbit_client.channel = rabbit_connection.channel
    app.state.rabbit_client = rabbit_client
    yield
    await rabbit_connection.close()

app = FastAPI(title='Инди Сервис', lifespan=lifespan)


app.include_router(comments_router, prefix='/comments', tags=['Comments'])
app.include_router(likes_router, prefix='/likes', tags=['Likes'])
app.include_router(posts_router, prefix='/posts', tags=['Posts'])
