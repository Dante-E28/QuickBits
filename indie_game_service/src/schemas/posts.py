from datetime import time
from pydantic import BaseModel


class PostsSchemaBase(BaseModel):
    name: str
    description: str
    user_id: int
    date_create: time


class PostsSchema(PostsSchemaBase):
    id: int

    class Config:
        from_attributes = True


class PostsSchemaAdd(PostsSchemaBase):
    pass


class PostsSchemaUpdate(PostsSchemaBase):
    pass
