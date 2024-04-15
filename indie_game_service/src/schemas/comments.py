from datetime import datetime
from pydantic import BaseModel


class CommentsSchemaBase(BaseModel):
    user_id: int
    text: str
    post_id: int


class CommentsSchema(CommentsSchemaBase):
    id: int
    date_create: datetime

    class Config:
        from_attributes = True


class CommentsSchemaAdd(CommentsSchemaBase):
    pass


class CommentsSchemaUpdate(BaseModel):
    text: str | None = None
