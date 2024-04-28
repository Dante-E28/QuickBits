from typing import Annotated

from fastapi import Depends, HTTPException, status

from src.schemas import UserCreate, UserRead
from src.unitofwork import IUnitOfWork, UnitOfWork
from src.utils import hash_password, validate_password


UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]


class UserService:
    @staticmethod
    async def register_user(
        uow: IUnitOfWork,
        user_in: UserCreate
    ) -> UserRead:
        async with uow:
            check = await uow.users.get(username=user_in.username)
            if check:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail={'User not found.'}
                )
            hashed_password = hash_password(user_in.password)
            data = user_in.model_dump(exclude={'password'})
            data.update(hashed_password=hashed_password)
            user = await uow.users.add(data)
            await uow.commit()
            return UserRead.model_validate(user)

    @staticmethod
    async def get_user(
        uow: IUnitOfWork,
        username: str
    ) -> UserRead | None:
        async with uow:
            user = await uow.users.get(username=username)
            return UserRead.model_validate(user)


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
