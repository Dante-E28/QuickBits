from datetime import datetime
import uuid
from pydantic import BaseModel


class CommentsSchemaBase(BaseModel):
    user_id: uuid.UUID
    text: str


class CommentsSchema(CommentsSchemaBase):
    id: int
    post_id: int
    date_create: datetime

    class Config:
        from_attributes = True


class CommentsSchemaAdd(CommentsSchemaBase):
    post_id: int


class CommentsSchemaUpdate(BaseModel):
    text: str | None = None
