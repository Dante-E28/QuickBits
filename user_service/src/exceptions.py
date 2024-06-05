import uuid
from fastapi import HTTPException, status


class InvalidCredentialsError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={'msg': 'Invalid username or password.'}
        )


class InvalidTokenCustomError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={'msg': 'Invalid token.'}
        )


class InvalidTokenTypeError(HTTPException):
    def __init__(self, token_type: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={'msg': f'Token type not {token_type!r}.'}
        )


class NotAuthenticatedError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )


class UserNotVerifiedError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={'msg': 'Email not verified.'}
        )


class UserNotActiveError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={'msg': 'User is not active.'}
        )


class UserAlreadyExistsError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail={'msg': 'User already exists.'}
        )


class NotPrivilegesError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={'msg': 'Not enough privileges.'}
        )


class EntityNotFoundError(HTTPException):
    def __init__(self, entity_type: str, entity_id: uuid.UUID):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'{entity_type} id: {entity_id} not found'
        )


class EntityAlreadyExistsError(HTTPException):
    def __init__(self, entity_type: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f'{entity_type} already exists'
        )
