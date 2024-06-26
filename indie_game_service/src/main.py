from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from src.rabbitmq.client import rabbit_connection, rabbit_client
from src.redis_cache import RouterCacheControlResetMiddleware, no_uow_key_builder
from src.routers.comments_router import router as comments_router
from src.routers.likes_router import router as likes_router
from src.routers.posts_router import router as posts_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await rabbit_connection.connect()
    rabbit_client.channel = rabbit_connection.channel
    app.state.rabbit_client = rabbit_client
    redis = aioredis.from_url('redis://localhost:6379')
    FastAPICache.init(
        RedisBackend(redis),
        prefix='indie',
        key_builder=no_uow_key_builder
    )
    yield
    await rabbit_connection.close()

app = FastAPI(title='Инди Сервис', lifespan=lifespan)

origins = [
    'http://localhost:5173'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'DELETE', 'PATCH'],
    allow_headers=[
        'Content-Type', 'Set-Cookie',
        'Access-Control-Allow-Headers', 'Access-Control-Allow-Origin'
    ],
)
app.add_middleware(RouterCacheControlResetMiddleware)


app.include_router(comments_router, prefix='/comments', tags=['Comments'])
app.include_router(likes_router, prefix='/likes', tags=['Likes'])
app.include_router(posts_router, prefix='/posts', tags=['Posts'])
