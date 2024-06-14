from datetime import datetime, timedelta, timezone
from typing import Any, cast

import bcrypt
from fastapi import Request, Response
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
import jwt
from jwt.exceptions import InvalidTokenError

from src.config import settings
from src.constants import (
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
    SECONDS_IN_DAY,
    SECONDS_IN_MINUTE
)
from src.exceptions import InvalidTokenCustomError, NotAuthenticatedError
from src.users.schemas import UserRead


class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        token_type: str,
        scheme_name: str | None = None,
        scopes: dict[str, str] | None = None,
        description: str | None = None,
        auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(
            password=cast(Any, {"tokenUrl": tokenUrl, "scopes": scopes})
        )
        self.token_type = token_type
        super().__init__(
            flows=flows,
            scheme_name=scheme_name,
            description=description,
            auto_error=auto_error,
        )

    async def __call__(self, request: Request) -> str | None:
        authorization = request.cookies.get(self.token_type)
        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise NotAuthenticatedError
            else:
                return None
        return param


def hash_password(password: str) -> bytes:
    salt: bytes = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)


def validate_password(plain_password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(
        password=plain_password.encode(),
        hashed_password=hashed_password
    )


def encode_jwt(
    payload: dict[str, Any],
    private_key: str = settings.auth_settings.private_key_path.read_text(),
    algorithm: str = settings.auth_settings.algorithm,
    expire_minutes: int = settings.auth_settings.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
) -> str:
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        iat=now,
        exp=expire
    )
    return jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm
    )


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_settings.public_key_path.read_text(),
    algorithm: str = settings.auth_settings.algorithm,
):
    return jwt.decode(token, public_key, algorithms=[algorithm])


ACCESS_EXPIRE = settings.auth_settings.access_token_expire_minutes
REFRESH_EXPIRE = settings.auth_settings.refresh_token_expire_days


def set_cookies(
    response: Response,
    access_token: str | None = None,
    refresh_token: str | None = None
) -> None:
    """Set cookies in response."""
    if access_token:
        response.set_cookie(
            key=ACCESS_TOKEN_TYPE,
            value='Bearer ' + access_token,
            max_age=ACCESS_EXPIRE * SECONDS_IN_MINUTE,
            httponly=True,
            secure=True,
            samesite='strict'
        )

    if refresh_token:
        response.set_cookie(
            key=REFRESH_TOKEN_TYPE,
            value='Bearer ' + refresh_token,
            max_age=REFRESH_EXPIRE * SECONDS_IN_DAY,
            httponly=True,
            secure=True,
            samesite='strict'
        )


def get_payload_from_token(token: str) -> dict:
    try:
        payload = decode_jwt(token)
    except InvalidTokenError:
        raise InvalidTokenCustomError
    return payload


def get_roles_for_payload(user: UserRead) -> list[str]:
    """Get list of roles for token payload."""
    roles: list = []
    if user.is_active:
        roles.append('is_active')
    if user.is_verified:
        roles.append('is_verified')
    if user.is_superuser:
        roles.append('is_superuser')
    return roles


def get_sub_from_payload(payload: dict) -> str:
    """Gets sub from payload or raise."""
    sub: str | None = payload.get('sub')
    if not sub:
        raise InvalidTokenCustomError
    return sub
