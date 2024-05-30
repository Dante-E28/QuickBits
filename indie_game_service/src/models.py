from datetime import datetime
import uuid
from pydantic import BaseModel
from typing import Annotated, TypeVar

from sqlalchemy import (DateTime, ForeignKey, String, func)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Model


intpk = Annotated[int, mapped_column(primary_key=True)]
SchemaResponse = TypeVar('SchemaResponse', bound=BaseModel)


class Posts(Model):
    __tablename__ = 'posts'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str]
    user_id: Mapped[uuid.UUID]
    date_create: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
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
    user_id: Mapped[uuid.UUID]
    text: Mapped[str]
    date_create: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    post: Mapped['Posts'] = relationship(
        back_populates='comments',
    )


class Likes(Model):
    __tablename__ = 'likes'

    id: Mapped[intpk]
    post_id: Mapped[int] = mapped_column(
        ForeignKey('posts.id')
    )
    user_id: Mapped[uuid.UUID]
    post: Mapped['Posts'] = relationship(
        back_populates='likes',
    )
