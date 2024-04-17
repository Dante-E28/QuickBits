from datetime import datetime
from pydantic import BaseModel, PositiveInt


class PostsSchemaBase(BaseModel):
    name: str
    user_id: PositiveInt
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
