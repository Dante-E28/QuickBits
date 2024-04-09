from datetime import time
from pydantic import BaseModel
from typing import Annotated, Type, TypeVar

from sqlalchemy import (ForeignKey, String)
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


intpk = Annotated[int, mapped_column(primary_key=True)]
SchemaResponse = TypeVar('SchemaResponse', bound=BaseModel)


class Posts(Base):
    __tablename__ = 'posts'

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str]
    user_id: Mapped[int]
    date_create: Mapped[time]

    def to_read_model(self, schema: Type[SchemaResponse]) -> SchemaResponse:
        return schema(
            id=self.id,
            name=self.name,
            description=self.description,
            user_id=self.user_id,
            date_create=self.date_create
        )


class Comments(Base):
    __tablename__ = 'comments'

    id: Mapped[intpk]
    post_id: Mapped[int] = mapped_column(
        ForeignKey('posts.id')
    )
    user_id: Mapped[int]
    text: Mapped[str]
    date_create: Mapped[time]

    def to_read_model(self, schema: Type[SchemaResponse]) -> SchemaResponse:
        return schema(
            id=self.id,
            post_id=self.post_id,
            user_id=self.user_id,
            text=self.text,
            date_create=self.date_create
        )


class Likes(Base):
    __tablename__ = 'likes'

    id: Mapped[intpk]
    post_id: Mapped[int] = mapped_column(
        ForeignKey('posts.id')
    )
    user_id: Mapped[int]

    def to_read_model(self, schema: Type[SchemaResponse]) -> SchemaResponse:
        return schema(
            id=self.id,
            post_id=self.post_id,
            user_id=self.user_id
        )
