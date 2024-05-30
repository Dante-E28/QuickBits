from datetime import datetime
import uuid
from pydantic import BaseModel


class PostsSchemaBase(BaseModel):
    name: str
    user_id: uuid.UUID
    description: str


class PostsSchema(PostsSchemaBase):
    id: int
    date_create: datetime

    class Config:
        from_attributes = True


class PostsSchemaAdd(PostsSchemaBase):
    pass


class PostsSchemaUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
