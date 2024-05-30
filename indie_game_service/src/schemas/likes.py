import uuid
from pydantic import BaseModel, PositiveInt


class LikesSchemaBase(BaseModel):
    post_id: PositiveInt
    user_id: uuid.UUID


class LikesSchema(LikesSchemaBase):
    id: int

    class Config:
        from_attributes = True


class LikesSchemaAdd(LikesSchemaBase):
    pass


class LikesSchemaDelete(LikesSchemaBase):
    pass
