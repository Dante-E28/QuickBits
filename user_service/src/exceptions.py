import uuid
from fastapi import HTTPException, status

from src.error_messages import (
    EMAIL_NOT_VERIFIED,
    ENTITY_ALREADY_EXISTS,
    ENTITY_NOT_FOUND,
    INVALID_CREDENTIALS,
    INVALID_TOKEN,
    INVALID_TOKEN_TYPE,
    NOT_ACTIVE,
    NOT_AUTHENTICATED,
    NOT_PRIVILEGES,
    USER_ALREADY_EXISTS
)


class InvalidCredentialsError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={'msg': INVALID_CREDENTIALS}
        )


class InvalidTokenCustomError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={'msg': INVALID_TOKEN}
        )


class InvalidTokenTypeError(HTTPException):
    def __init__(self, token_type: str):
        msg = INVALID_TOKEN_TYPE.format(token_type=token_type)
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={'msg': msg}
        )


class NotAuthenticatedError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={'msg': NOT_AUTHENTICATED},
            headers={'WWW-Authenticate': 'Bearer'},
        )


class UserNotVerifiedError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={'msg': EMAIL_NOT_VERIFIED}
        )


class UserNotActiveError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={'msg': NOT_ACTIVE}
        )


class UserAlreadyExistsError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail={'msg': USER_ALREADY_EXISTS}
        )


class NotPrivilegesError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={'msg': NOT_PRIVILEGES}
        )


class EntityNotFoundError(HTTPException):
    def __init__(self, entity_type: str, entity_id: uuid.UUID):
        msg = ENTITY_NOT_FOUND.format(
            entity_type=entity_type,
            entity_id=entity_id
        )
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'msg': msg}
        )


class EntityAlreadyExistsError(HTTPException):
    def __init__(self, entity_type: str):
        msg = ENTITY_ALREADY_EXISTS.format(entity_type=entity_type)
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'msg': msg}
        )


class ValidationCustomError(HTTPException):
    def __init__(self, msg: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={'msg': msg}
        )
