from fastapi import HTTPException, status

from src.constants import ACCESS_TOKEN_TYPE


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
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={'msg': f'Token type not {ACCESS_TOKEN_TYPE!r}.'}
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


class NotPrivilegesError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={'msg': 'Not enough privileges.'}
        )
