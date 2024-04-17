from datetime import datetime
from pydantic import BaseModel, PositiveInt


class CommentsSchemaBase(BaseModel):
    user_id: PositiveInt
    text: str


class CommentsSchema(CommentsSchemaBase):
    id: int
    post_id: int
    date_create: datetime

    class Config:
        from_attributes = True


class CommentsSchemaAdd(CommentsSchemaBase):
    pass


class CommentsSchemaUpdate(BaseModel):
    text: str | None = None
