from fastapi import HTTPException, status

from src.error_messages import (
    ENTITY_ALREADY_EXISTS,
    ENTITY_NOT_FOUND,
    INVALID_TOKEN,
    NOT_AUTHENTICATED,
    NOT_PRIVILEGES
)


class EntityNotFoundError(HTTPException):
    def __init__(self, entity_type: str, entity_id: int):
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


class InvalidTokenCustomError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={'msg': INVALID_TOKEN}
        )


class NotAuthenticatedError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={'msg': NOT_AUTHENTICATED},
            headers={'WWW-Authenticate': 'Bearer'}
        )


class NotPrivilegesError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={'msg': NOT_PRIVILEGES}
        )
