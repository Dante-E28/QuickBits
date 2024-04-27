from uuid import UUID
from pydantic import BaseModel


class UsersSchemaBase(BaseModel):
    username: str
    email: str | None = None
    hashed_password: bytes


class UsersSchema(UsersSchemaBase):
    id: UUID
    is_active: bool
    is_verified: bool
    is_superuser: bool


class UsersSchemaAdd(UsersSchemaBase):
    pass
