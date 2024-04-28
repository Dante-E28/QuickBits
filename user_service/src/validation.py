from src.constants import TOKEN_TYPE_FIELD
from src.exceptions import InvalidTokenTypeError


def validate_token_type(
    payload: dict,
    token_type: str
) -> bool:
    """True if correct token type or raise InvalidTokenTypeError."""
    if payload.get(TOKEN_TYPE_FIELD) == token_type:
        return True
    raise InvalidTokenTypeError(token_type)
