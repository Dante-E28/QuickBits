from pydantic import BaseModel, PositiveInt


class LikesSchemaBase(BaseModel):
    post_id: PositiveInt
    user_id: PositiveInt


class LikesSchema(LikesSchemaBase):
    id: int

    class Config:
        from_attributes = True


class LikesSchemaAdd(LikesSchemaBase):
    pass
