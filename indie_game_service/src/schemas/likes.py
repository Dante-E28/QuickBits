from pydantic import BaseModel


class LikesSchemaBase(BaseModel):
    post_id: int
    user_id: int


class LikesSchema(LikesSchemaBase):
    id: int

    class Config:
        from_attributes = True


class LikesSchemaAdd(LikesSchemaBase):
    pass
