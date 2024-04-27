from sqlalchemy import UUID, String, BINARY
from src.database import Model
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Annotated, TypeVar

intpk = Annotated[int, mapped_column(primary_key=True)]


class Users(Model):
    __tablename__ = 'users'

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    hashed_password: Mapped[bytes] = mapped_column(BINARY(64), nullable=False)
    is_active: Mapped[bool]
    is_verified: Mapped[bool]
    is_superuser: Mapped[bool]
