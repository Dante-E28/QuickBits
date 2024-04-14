from contextlib import asynccontextmanager
from fastapi import FastAPI

from src.database import create_table
from src.routers.comments_router import router as comments_router
from src.routers.likes_router import router as likes_router
from src.routers.posts_router import router as posts_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_table()
    yield
    print('Конец приложения')

app = FastAPI(title='Инди Сервис', lifespan=lifespan)


app.include_router(comments_router, prefix='/comments', tags=['Comments'])
app.include_router(likes_router, prefix='/likes', tags=['Likes'])
app.include_router(posts_router, prefix='/posts', tags=['Posts'])
