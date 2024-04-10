from datetime import time
from pydantic import BaseModel


class PostsSchema(BaseModel):
    name: str
    description: str
    user_id: int
    date_create: time
