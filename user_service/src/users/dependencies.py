from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError

from src.constants import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE
from src.exceptions import (
    InvalidCredentialsError,
    InvalidTokenCustomError,
    NotPrivilegesError,
    UserNotActiveError,
    UserNotVerifiedError
)
from src.users.schemas import UserRead
from src.users.services import AuthService
from src.users.utils import decode_jwt
from src.repositories.unitofwork import IUnitOfWork, UnitOfWork
from src.users.validation import validate_token_type


UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]
oauth2_schema = OAuth2PasswordBearer(tokenUrl='/auth/login')


def get_current_payload(
    token: Annotated[str, Depends(oauth2_schema)]
) -> dict:
    try:
        payload = decode_jwt(token)
    except InvalidTokenError:
        raise InvalidTokenCustomError
    return payload


async def get_current_user(
    uow: UOWDep,
    payload: dict = Depends(get_current_payload)
) -> UserRead:
    validate_token_type(payload, ACCESS_TOKEN_TYPE)
    return await AuthService.get_user_by_token_sub(uow, payload)


async def get_current_user_for_refresh(
    uow: UOWDep,
    payload: dict = Depends(get_current_payload)
) -> UserRead:
    validate_token_type(payload, REFRESH_TOKEN_TYPE)
    return await AuthService.get_user_by_token_sub(uow, payload)


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


async def validate_auth_user(
    uow: UOWDep,
    credentials: Annotated[OAuth2PasswordRequestForm, Depends()]
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
