from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt.exceptions import InvalidTokenError

from src.constants import ACCESS_TOKEN_TYPE, TOKEN_TYPE_FIELD
from src.exceptions import (
    InvalidCredentialsError,
    InvalidTokenCustomError,
    InvalidTokenTypeError,
    NotPrivilegesError,
    UserNotActiveError,
    UserNotVerifiedError
)
from src.fake_service import UserService
from src.schemas import UserRead
from src.services import AuthService
from src.utils import decode_jwt
from src.unitofwork import IUnitOfWork, UnitOfWork


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
    token_type = payload.get(TOKEN_TYPE_FIELD)
    if token_type != ACCESS_TOKEN_TYPE:
        raise InvalidTokenTypeError
    username: str | None = payload.get('sub')
    if not username:
        raise InvalidTokenCustomError
    user = await UserService.get_user(uow, username)
    if not user:
        raise InvalidTokenCustomError
    if not user.is_verified:
        raise UserNotVerifiedError
    return UserRead.model_validate(user)


async def get_active_user(
    current_user: UserRead = Depends(get_current_user)
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
