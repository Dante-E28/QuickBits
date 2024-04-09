from datetime import time
from pydantic import BaseModel
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class PostsSchema(BaseModel):
    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str]
    user_id: Mapped[int]
    date_create: Mapped[time]
