from typing import Annotated
import uuid

from fastapi import Depends, Path, Request
from fastapi.security import OAuth2PasswordRequestForm

from src.constants import (
    ACCESS_TOKEN_TYPE,
    EMAIL_VERIFICATION_TOKEN_TYPE,
    PASSWORD_RESET_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE
)
from src.limiter import limiter
from src.exceptions import (
    InvalidCredentialsError,
    NotPrivilegesError,
    UserNotActiveError,
    UserNotVerifiedError
)
from src.users.schemas import UserRead
from src.users.services import AuthService, UserService
from src.users.utils import (
    OAuth2PasswordBearerWithCookie,
    get_payload_from_token
)
from src.repositories.unitofwork import IUnitOfWork, UnitOfWork
from src.users.validation import validate_token_type


UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]
oauth2_schema_cookie = OAuth2PasswordBearerWithCookie(
    tokenUrl='/auth/token', token_type=ACCESS_TOKEN_TYPE)
oauth2_schema_cookie_refresh = OAuth2PasswordBearerWithCookie(
    tokenUrl='/refresh_token', token_type=REFRESH_TOKEN_TYPE)


def get_current_payload(
    token: Annotated[str, Depends(oauth2_schema_cookie)]
) -> dict:
    return get_payload_from_token(token)


def get_current_payload_for_refresh(
    token: Annotated[str, Depends(oauth2_schema_cookie_refresh)]
) -> dict:
    return get_payload_from_token(token)


def get_current_payload_from_email_token(
    token: Annotated[str, Path]
) -> dict:
    return get_payload_from_token(token)


async def get_current_user(
    uow: UOWDep,
    payload: dict = Depends(get_current_payload)
) -> UserRead:
    validate_token_type(payload, ACCESS_TOKEN_TYPE)
    return await AuthService.get_user_by_token_sub(uow, payload)


async def get_current_user_for_refresh(
    uow: UOWDep,
    payload: dict = Depends(get_current_payload_for_refresh)
) -> UserRead:
    validate_token_type(payload, REFRESH_TOKEN_TYPE)
    return await AuthService.get_user_by_token_sub(uow, payload)


async def verify_current_user(
    uow: UOWDep,
    payload: dict = Depends(get_current_payload_from_email_token)
) -> UserRead:
    validate_token_type(payload, EMAIL_VERIFICATION_TOKEN_TYPE)
    return await AuthService.verify_user_email_by_payload(uow, payload)


async def get_reset_password_user(
    uow: UOWDep,
    payload: dict = Depends(get_current_payload_from_email_token)
) -> UserRead:
    validate_token_type(payload, PASSWORD_RESET_TOKEN_TYPE)
    return await AuthService.get_user_by_token_sub_email(uow, payload)


async def get_verified_user(
    current_user: UserRead = Depends(get_current_user)
) -> UserRead:
    if not current_user.is_verified:
        raise UserNotVerifiedError
    return current_user


async def get_active_user(
    current_user: UserRead = Depends(get_verified_user)
) -> UserRead:
    if not current_user.is_active:
        raise UserNotActiveError
    return current_user


async def get_superuser(
    current_user: UserRead = Depends(get_active_user)
) -> UserRead:
    if not current_user.is_superuser:
        raise NotPrivilegesError
    return current_user


@limiter.limit('5 per 30 minute')
async def validate_auth_user(
    uow: UOWDep,
    credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    request: Request  # for limiter
) -> UserRead:
    """Gets user by credentials."""
    user = await AuthService.authenticate_user(
        uow=uow,
        username=credentials.username,
        password=credentials.password
    )
    if not user:
        raise InvalidCredentialsError
    return user


async def validate_user_email(
    uow: UOWDep,
    email: str
) -> UserRead | None:
    """Gets user by email."""
    user = await UserService.get_users(uow=uow, email=email)
    if user:
        return user[0]
    return None


async def no_cache_get_user(uow: UOWDep, user_id: uuid.UUID):
    return await UserService.get_user(uow, user_id)
