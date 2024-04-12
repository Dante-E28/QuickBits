from datetime import time
from pydantic import BaseModel
from typing import Annotated, TypeVar

from sqlalchemy import (ForeignKey, String)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Model


intpk = Annotated[int, mapped_column(primary_key=True)]
SchemaResponse = TypeVar('SchemaResponse', bound=BaseModel)


class Posts(Model):
    __tablename__ = 'posts'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str]
    user_id: Mapped[int]
    date_create: Mapped[time]
    comments: Mapped[list['Comments']] = relationship(
        back_populates='post',
        cascade='all, delete'
    )
    likes: Mapped[list['Likes']] = relationship(
        back_populates='post',
        cascade='all, delete'
    )


class Comments(Model):
    __tablename__ = 'comments'

    id: Mapped[intpk]
    post_id: Mapped[int] = mapped_column(
        ForeignKey('posts.id')
    )
    user_id: Mapped[int]
    text: Mapped[str]
    date_create: Mapped[time]
    post: Mapped['Posts'] = relationship(
        back_populates='comments',
    )


class Likes(Model):
    __tablename__ = 'likes'

    id: Mapped[intpk]
    post_id: Mapped[int] = mapped_column(
        ForeignKey('posts.id')
    )
    user_id: Mapped[int]
    post: Mapped['Posts'] = relationship(
        back_populates='likes',
    )
