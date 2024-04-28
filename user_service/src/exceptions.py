from fastapi import HTTPException, status


class InvalidCredentialsError(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={'msg': 'Invalid username or password.'}
        )
