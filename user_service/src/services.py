from datetime import timedelta

from src.exceptions import InvalidTokenCustomError
from src.fake_service import UserService
from src.config import settings
from src.constants import (
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
    TOKEN_TYPE_FIELD
)
from src.unitofwork import IUnitOfWork
from src.schemas import UserRead, UserCreate
from src.utils import encode_jwt, validate_password


class UsersService:

    @staticmethod
    async def add_user(
        uow: IUnitOfWork,
        user: UserCreate
    ) -> UserRead:
        async with uow:
            result = await uow.users.add(user.model_dump())
            await uow.commit()
            return UserRead.model_validate(result)


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
        user = await UserService.get_user(uow, username)
        if not user:
            raise InvalidTokenCustomError
        return UserRead.model_validate(user)
