from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from exceptions import InvalidCredentialsError
from fake_service import UOWDep, AuthService
from schema import Token
from utils import encode_jwt


router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/login')
async def login(
    uow: UOWDep,
    credentials: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = await AuthService.authenticate_user(
        uow,
        credentials.username
    )
    if not user:
        raise InvalidCredentialsError
    payload: dict = {
        'sub': credentials.username,
    }
    token = encode_jwt(payload)
    return Token(
        access_token=token,
        token_type='Bearer'
    )
