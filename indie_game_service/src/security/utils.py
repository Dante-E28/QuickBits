import jwt

from src.config import settings


def decode_jwt(
    token: str | bytes,
    public_key: str,
    algorithm: str = settings.ALGORITHM,
):
    return jwt.decode(token, public_key, algorithms=[algorithm])
