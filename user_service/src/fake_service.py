from typing import Annotated

from fastapi import Depends

from schema import UserRead
from unitofwork import IUnitOfWork, UnitOfWork
from utils import validate_password


UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]


class AuthService:
    @staticmethod
    async def authenticate_user(
            uow: IUnitOfWork,
            username: str,
            password: str
    ) -> UserRead | None:
        async with uow:
            user = await uow.users.get(username=username)
            if user and validate_password(password, user.hashed_password):
                return UserRead.model_validate(user)
            return None
