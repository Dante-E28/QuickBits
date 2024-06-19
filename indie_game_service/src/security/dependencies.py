from pathlib import Path

from fastapi import Depends
from fastapi.security.utils import get_authorization_scheme_param
from fastapi.requests import Request
from jwt.exceptions import InvalidTokenError

from src.config import settings
from src.exceptions import (
    InvalidTokenCustomError,
    NotAuthenticatedError,
    NotPrivilegesError
)
from src.security.enum import Roles
from src.security.utils import decode_jwt


BASE_DIR = Path(__file__).parent.parent.parent
public_key_path = BASE_DIR / 'certs' / 'public.pem'


def get_public_key() -> str:
    return public_key_path.read_text()


def get_access_token(request: Request) -> str:
    token_data: str | None = request.cookies.get(settings.ACCESS_TOKEN_TYPE)
    schema, token = get_authorization_scheme_param(token_data)
    if not token or schema.lower() != 'bearer':
        raise NotAuthenticatedError
    return token


def get_payload(token: str = Depends(get_access_token)) -> dict:
    public_key = get_public_key()
    try:
        payload: dict = decode_jwt(token, public_key)
    except InvalidTokenError:
        raise InvalidTokenCustomError
    return payload


def get_common_permission(payload: dict = Depends(get_payload)) -> list:
    """Check common roles in payload from token."""
    roles: list | None = payload.get('roles')
    token_type: str | None = payload.get('type')
    if not roles or not token_type:
        raise InvalidTokenCustomError
    if Roles.VERIFIED.value not in roles:
        raise NotPrivilegesError
    return roles


def get_superuser_permission(
    roles: list = Depends(get_common_permission)
) -> None:
    """Check is token from superuser."""
    if Roles.SUPERUSER.value not in roles:
        raise NotPrivilegesError
