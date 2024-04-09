from sqlalchemy.ext.asyncio import async_sessionmaker
from fastapi import FastAPI

from src.database import engine


app = FastAPI(title='Инди Сервис')

session = async_sessionmaker(bind=engine, expire_on_commit=False)
