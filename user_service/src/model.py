from uuid import UUID, uuid4
from sqlalchemy import String
from src.database import Model
from sqlalchemy.orm import Mapped, mapped_column


class Users(Model):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(primary_key=True)
    hashed_password: Mapped[bytes]
    is_active: Mapped[bool] = mapped_column(default=False)
    is_verified: Mapped[bool] = mapped_column(default=False)
    is_superuser: Mapped[bool] = mapped_column(default=False)
