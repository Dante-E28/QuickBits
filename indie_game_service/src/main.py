from fastapi import FastAPI

from src.routers.comments_router import router as comments_router
from src.routers.likes_router import router as likes_router
from src.routers.posts_router import router as posts_router

app = FastAPI(title='Инди Сервис')


app.include_router(comments_router)
app.include_router(likes_router)
app.include_router(posts_router)
