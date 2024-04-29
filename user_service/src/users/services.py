from datetime import timedelta
import uuid

from src.exceptions import EntityNotFoundError, InvalidTokenCustomError
from src.config import settings
from src.constants import (
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
    TOKEN_TYPE_FIELD
)
from src.repositories.unitofwork import IUnitOfWork
from src.users.schemas import UserRead, UserCreate, UserUpdate
from src.users.utils import encode_jwt, validate_password, hash_password


class UserService:

    @staticmethod
    async def register_user(
        uow: IUnitOfWork,
        user_in: UserCreate
    ) -> UserRead:
        hashed_password = hash_password(user_in.password)
        data = user_in.model_dump(exclude={'password'})
        data['hashed_password'] = hashed_password
        async with uow:
            result = await uow.users.add(data)
            await uow.commit()
            return UserRead.model_validate(result)

    @staticmethod
    async def get_user(
        uow: IUnitOfWork,
        user_id: uuid.UUID
    ) -> UserRead:
        async with uow:
            result = await uow.users.get(id=user_id)
            if result:
                return UserRead.model_validate(result)
            else:
                raise EntityNotFoundError('User', user_id)

    @staticmethod
    async def get_user_by_username(
        uow: IUnitOfWork,
        username: str
    ) -> UserRead:
        async with uow:
            result = await uow.users.get(username=username)
            return UserRead.model_validate(result)

    @staticmethod
    async def get_users(
        uow: IUnitOfWork,
    ) -> list[UserRead]:
        async with uow:
            users = await uow.users.get_all()
            return [UserRead.model_validate(user) for user in users]

    @staticmethod
    async def edit_user(
        uow: IUnitOfWork,
        user_update: UserUpdate,
        user_id: uuid.UUID
    ) -> UserRead:
        if user_update.password:
            hashed_password = hash_password(user_update.password)
            data = user_update.model_dump(
                exclude={'password'}, exclude_none=True
            )
            data['hashed_password'] = hashed_password
        async with uow:
            result = await uow.users.update(data, id=user_id)
            await uow.commit()
            return UserRead.model_validate(result)

    @staticmethod
    async def edit_me(
        uow: IUnitOfWork,
        user_update: UserUpdate,
        user_id: uuid.UUID
    ) -> UserRead:
        if user_update.password:
            hashed_password = hash_password(user_update.password)
            data = user_update.model_dump(
                exclude={'password'}, exclude_none=True
            )
            data['hashed_password'] = hashed_password
        async with uow:
            result = await uow.users.update(data, id=user_id)
            await uow.commit()
            return UserRead.model_validate(result)

    @staticmethod
    async def delete_user(
        uow: IUnitOfWork,
        user_id: uuid.UUID
    ) -> None:
        async with uow:
            await uow.users.delete(id=user_id)
            await uow.commit()

    @staticmethod
    async def delete_me(
        uow: IUnitOfWork,
        user_id: uuid.UUID
    ) -> None:
        async with uow:
            await uow.users.delete(id=user_id)
            await uow.commit()


class AuthService:
    @staticmethod
    def _create_jwt(
        token_type: str,
        token_data: dict,
        expire_min: int = settings.auth_settings.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None
    ) -> str:
        """Create jwt from data."""
        payload: dict = {
            TOKEN_TYPE_FIELD: token_type
        }
        payload.update(token_data)
        return encode_jwt(
            payload=payload,
            expire_minutes=expire_min,
            expire_timedelta=expire_timedelta
        )

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

    @staticmethod
    def create_access_token(
        user: UserRead
    ) -> str:
        """Create access token by user."""
        payload: dict = {
            'sub': user.username,
            'username': user.username,
            'email': user.email
        }
        return AuthService._create_jwt(
            token_type=ACCESS_TOKEN_TYPE,
            token_data=payload,
            expire_min=settings.auth_settings.access_token_expire_minutes
        )

    @staticmethod
    def create_refresh_token(
        user: UserRead
    ) -> str:
        """Create refresh token by user."""
        payload: dict = {
            'sub': user.username
        }
        return AuthService._create_jwt(
            token_type=REFRESH_TOKEN_TYPE,
            token_data=payload,
            expire_timedelta=timedelta(
                days=settings.auth_settings.refresh_token_expire_days)
        )

    @staticmethod
    async def get_user_by_token_sub(
        uow: IUnitOfWork,
        payload: dict
    ) -> UserRead:
        """Gets user from token 'sub'."""
        username: str | None = payload.get('sub')
        if not username:
            raise InvalidTokenCustomError
        user = await UserService.get_user_by_username(uow, username)
        if not user:
            raise InvalidTokenCustomError
        return UserRead.model_validate(user)
