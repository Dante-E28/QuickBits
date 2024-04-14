from datetime import datetime, timezone
from pydantic import BaseModel


class PostsSchemaBase(BaseModel):
    name: str
    user_id: int
    description: str


class PostsSchema(PostsSchemaBase):
    id: int
    date_create: datetime

    class Config:
        from_attributes = True


class PostsSchemaAdd(PostsSchemaBase):
    pass


class PostsSchemaUpdate(PostsSchemaBase):
    name: str | None = None
    description: str | None = None
