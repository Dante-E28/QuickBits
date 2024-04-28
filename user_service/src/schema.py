import uuid

from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class UserBase(BaseModel):
    username: str | None = None
    email: EmailStr | None = None


class UserCreate(BaseModel):
    username: str
    password: str


class UserUpdate(BaseModel):
    password: str | None = None


class UserRead(BaseModel):
    id: uuid.UUID
    username: str
    email: EmailStr
    is_active: bool
    is_verified: bool
    is_superuser: bool

    class Config:
        from_attributes = True
