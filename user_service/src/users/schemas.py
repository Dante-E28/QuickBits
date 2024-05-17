import uuid
from typing import Annotated

from annotated_types import MaxLen, MinLen
from pydantic import BaseModel, EmailStr

from src.users.mixin import PasswordValidatorMixin, UsernameValidatorMixin


class Token(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = 'Bearer'


class UserBase(BaseModel):
    username: str | None = None
    email: EmailStr | None = None


class UserCreate(
    UserBase,
    PasswordValidatorMixin,
    UsernameValidatorMixin
):
    username: Annotated[str, MinLen(4), MaxLen(16)]
    password: Annotated[str, MinLen(6)]


class UserUpdate(UserBase, PasswordValidatorMixin):
    password: str | None = None


class UserRead(UserBase):
    id: uuid.UUID
    username: str
    email: EmailStr

    is_active: bool
    is_verified: bool
    is_superuser: bool

    class Config:
        from_attributes = True


class MessageWithUser(BaseModel):
    user_id: str
