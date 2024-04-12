from datetime import time
from pydantic import BaseModel


class CommentsSchemaBase(BaseModel):
    post_id: int
    user_id: int
    text: str
    date_create: time


class CommentsSchema(CommentsSchemaBase):
    id: int

    class Config:
        from_attributes = True


class CommentsSchemaAdd(CommentsSchemaBase):
    pass
