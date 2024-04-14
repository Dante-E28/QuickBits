from datetime import datetime
from pydantic import BaseModel


class CommentsSchemaBase(BaseModel):
    user_id: int
    text: str


class CommentsSchema(CommentsSchemaBase):
    id: int
    post_id: int
    date_create: datetime

    class Config:
        from_attributes = True


class CommentsSchemaAdd(CommentsSchemaBase):
    pass


class CommentsSchemaUpdate(CommentsSchemaBase):
    text: str | None = None
