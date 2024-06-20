from datetime import timedelta
import uuid

from src.emails.utils import send_verify_email
from src.exceptions import (
    InvalidTokenCustomError, UserAlreadyExistsError, UserNotFoundError
)
from src.config import settings
from src.constants import (
    ACCESS_TOKEN_TYPE,
    EMAIL_TOKEN_HOURS,
    EMAIL_VERIFICATION_TOKEN_TYPE,
    PASSWORD_RESET_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
    RESET_PASSWORD_TOKEN_HOURS,
    TOKEN_TYPE_FIELD
)
from src.repositories.unitofwork import IUnitOfWork
from src.users.schemas import PasswordReset, UserRead, UserCreate, UserUpdate
from src.users.utils import (
    encode_jwt,
    get_roles_for_payload,
    get_sub_from_payload,
    validate_password,
    hash_password
)


class UserService:
    @classmethod
    async def _is_username_email_exists(
        cls,
        uow: IUnitOfWork,
        username: str | None = None,
        email: str | None = None
    ) -> bool:
        """Return True if username or email exists."""
        if username:
            if await uow.users.get(username=username):
                return True
        if email:
            if await uow.users.get(email=email):
                return True
        return False

    @classmethod
    async def register_user(
        cls,
        uow: IUnitOfWork,
        user_in: UserCreate
    ) -> UserRead:
        async with uow:
            if await cls._is_username_email_exists(
                uow=uow,
                username=user_in.username,
                email=user_in.email
            ):
                raise UserAlreadyExistsError
            hashed_password = hash_password(user_in.password)
            data = user_in.model_dump(exclude={'password'})
            data['hashed_password'] = hashed_password
            result = await uow.users.add(data)
            await uow.commit()
            user = UserRead.model_validate(result)
            # Send email verification
            token: str = AuthService.create_email_verification_token(user)
            send_verify_email(user.email, token)

            return user

    @staticmethod
    async def get_user(
        uow: IUnitOfWork,
        user_id: uuid.UUID
    ) -> UserRead:
        async with uow:
            user = await uow.users.get(id=user_id)
            if not user:
                raise UserNotFoundError(user_id)
            return UserRead.model_validate(user)

    @staticmethod
    async def get_user_by_username(
        uow: IUnitOfWork,
        username: str
    ) -> UserRead:
        async with uow:
            user = await uow.users.get(username=username)
            if not user:
                raise UserNotFoundError(username)
            return UserRead.model_validate(user)

    @staticmethod
    async def get_user_by_email(
        uow: IUnitOfWork,
        email: str
    ) -> UserRead:
        async with uow:
            user = await uow.users.get(email=email)
            if not user:
                raise UserNotFoundError(email)
            return UserRead.model_validate(user)

    @staticmethod
    async def verify_email(
        uow: IUnitOfWork,
        email: str
    ) -> UserRead:
        """Verify user email."""
        async with uow:
            user = await uow.users.get(email=email)
            if not user:
                raise UserNotFoundError(email)
            if not user.is_verified:
                user.is_verified = True
                await uow.commit()
            return UserRead.model_validate(user)

    @staticmethod
    async def get_users(
        uow: IUnitOfWork,
        **filters
    ) -> list[UserRead]:
        async with uow:
            users = await uow.users.get_all(**filters)
            return [UserRead.model_validate(user) for user in users]

    @classmethod
    async def edit_user(
        cls,
        uow: IUnitOfWork,
        user_update: UserUpdate,
        user_id: uuid.UUID
    ) -> UserRead:
        async with uow:
            if await cls._is_username_email_exists(
                uow=uow,
                username=user_update.username,
                email=user_update.email
            ):
                raise UserAlreadyExistsError
            data = user_update.model_dump(
                exclude={'password'}, exclude_none=True
            )
            if user_update.password:
                hashed_password = hash_password(user_update.password)
                data['hashed_password'] = hashed_password
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

    @staticmethod
    async def reset_password(
        uow: IUnitOfWork,
        user_id: uuid.UUID,
        password_in: PasswordReset
    ) -> None:
        """Change password."""
        async with uow:
            hashed_password = hash_password(password_in.password)
            data = {
                'hashed_password': hashed_password
            }
            await uow.users.update(data, id=user_id)
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
            'email': user.email,
            'roles': get_roles_for_payload(user)
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
    def create_email_verification_token(
        user: UserRead
    ) -> str:
        """Create token for email verification."""
        payload: dict = {
            'sub': user.email
        }
        return AuthService._create_jwt(
            token_type=EMAIL_VERIFICATION_TOKEN_TYPE,
            token_data=payload,
            expire_timedelta=timedelta(hours=EMAIL_TOKEN_HOURS)
        )

    @staticmethod
    def create_password_reset_token(
        user: UserRead
    ) -> str:
        """Create token for password reset."""
        payload: dict = {
            'sub': user.email
        }
        return AuthService._create_jwt(
            token_type=PASSWORD_RESET_TOKEN_TYPE,
            token_data=payload,
            expire_timedelta=timedelta(hours=RESET_PASSWORD_TOKEN_HOURS)
        )

    @staticmethod
    async def get_user_by_token_sub(
        uow: IUnitOfWork,
        payload: dict
    ) -> UserRead:
        """Gets user from token 'sub' username."""
        username: str = get_sub_from_payload(payload)
        user = await UserService.get_user_by_username(uow, username)
        if not user:
            raise InvalidTokenCustomError
        return UserRead.model_validate(user)

    @staticmethod
    async def verify_user_email_by_payload(
        uow: IUnitOfWork,
        payload: dict
    ) -> UserRead:
        """Verify user email by token 'sub' email."""
        email: str = get_sub_from_payload(payload)
        user = await UserService.verify_email(uow, email)
        return user

    @staticmethod
    async def get_user_by_token_sub_email(
        uow: IUnitOfWork,
        payload: dict
    ) -> UserRead:
        """Gets user from token 'sub' email."""
        email: str = get_sub_from_payload(payload)
        user = await UserService.get_user_by_email(uow, email)
        if not user:
            raise InvalidTokenCustomError
        return UserRead.model_validate(user)
