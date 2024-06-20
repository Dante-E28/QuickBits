from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from src.limiter import limiter, rate_limit_exceeded_handler
from src.rabbitmq.server import RabbitServer
from src.users.router import auth_router, user_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    rabbit_server = await RabbitServer.create_server()
    redis = aioredis.from_url('redis://localhost:6379')
    FastAPICache.init(RedisBackend(redis), prefix='fastapi-cache')
    yield
    await rabbit_server.close_connection()


app = FastAPI(title='Юзер Сервис', lifespan=lifespan)

# Limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# CORS
origins = [
    'http://localhost:5173'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['GET', 'POST', 'PATCH'],
    allow_headers=[
        'Content-Type', 'Set-Cookie',
        'Access-Control-Allow-Headers', 'Access-Control-Allow-Origin'
    ],
)

# Routers
app.include_router(auth_router)
app.include_router(user_router)
