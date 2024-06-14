import uuid
from fastapi import HTTPException, status

from src.error_messages import (
    EMAIL_NOT_SENDING,
    EMAIL_NOT_VERIFIED,
    ERROR_MESSAGE,
    INVALID_CREDENTIALS,
    INVALID_TOKEN,
    INVALID_TOKEN_TYPE,
    NOT_ACTIVE,
    NOT_AUTHENTICATED,
    NOT_PRIVILEGES,
    SMTP_SERVER_DOWN,
    USER_ALREADY_EXISTS,
    USER_NOT_FOUND
)


class InvalidCredentialsError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={ERROR_MESSAGE: INVALID_CREDENTIALS}
        )


class InvalidTokenCustomError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={ERROR_MESSAGE: INVALID_TOKEN}
        )


class InvalidTokenTypeError(HTTPException):
    def __init__(self, token_type: str):
        msg = INVALID_TOKEN_TYPE.format(token_type=token_type)
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={ERROR_MESSAGE: msg}
        )


class UserNotFoundError(HTTPException):
    def __init__(self, entity_data: str | uuid.UUID):
        msg = USER_NOT_FOUND.format(entity_data=entity_data)
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={ERROR_MESSAGE: msg}
        )


class NotAuthenticatedError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={ERROR_MESSAGE: NOT_AUTHENTICATED},
            headers={'WWW-Authenticate': 'Bearer'},
        )


class UserNotVerifiedError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={ERROR_MESSAGE: EMAIL_NOT_VERIFIED}
        )


class UserNotActiveError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={ERROR_MESSAGE: NOT_ACTIVE}
        )


class UserAlreadyExistsError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail={ERROR_MESSAGE: USER_ALREADY_EXISTS}
        )


class NotPrivilegesError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={ERROR_MESSAGE: NOT_PRIVILEGES}
        )


class ValidationCustomError(HTTPException):
    def __init__(self, msg: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={ERROR_MESSAGE: msg}
        )


class EmailNotSendingError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={ERROR_MESSAGE: EMAIL_NOT_SENDING}
        )


class SMTPServerNotAllowedError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail={ERROR_MESSAGE: SMTP_SERVER_DOWN}
        )
