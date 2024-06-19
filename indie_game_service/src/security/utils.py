import jwt
import logging

from src.config import settings

logger = logging.getLogger("uvicorn.error")


def decode_jwt(
    token: str | bytes,
    public_key: str,
    algorithm: str = settings.ALGORITHM,
):
    try:
        decoded = jwt.decode(token, public_key, algorithms=[algorithm])
        logger.info('ГУД')
        return decoded
    except jwt.PyJWTError as e:
        logger.error(f'ТУТЬ ПРОЕБ: {str(e)}')
        raise jwt.InvalidTokenError from e
