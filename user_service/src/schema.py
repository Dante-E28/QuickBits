<<<<<<< HEAD
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
=======
from uuid import UUID
from pydantic import BaseModel


class UsersSchemaBase(BaseModel):
    username: str
    email: str | None = None
    hashed_password: bytes


class UsersSchema(UsersSchemaBase):
    id: UUID
>>>>>>> a435e4e4936bd77d679c6ca29499fc73ee4a726e
    is_active: bool
    is_verified: bool
    is_superuser: bool

<<<<<<< HEAD
    class Config:
        from_attributes = True
=======

class UsersSchemaAdd(UsersSchemaBase):
    pass
>>>>>>> a435e4e4936bd77d679c6ca29499fc73ee4a726e
