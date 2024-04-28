from datetime import datetime, timedelta, timezone
from typing import Any

import bcrypt
import jwt

from src.config import settings


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
