from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from src.dependencies import get_current_user, oauth2_schema # noqa
from src.exceptions import InvalidCredentialsError
from src.fake_service import UOWDep, AuthService, UserService
from src.schemas import Token, UserCreate, UserRead
from src.utils import encode_jwt


auth_router = APIRouter(prefix='/auth', tags=['Auth'])
user_router = APIRouter(prefix='/user', tags=['User'])


@auth_router.post('/login')
async def login(
    uow: UOWDep,
    credentials: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = await AuthService.authenticate_user(
        uow,
        credentials.username,
        credentials.password
    )
    if not user:
        raise InvalidCredentialsError
    payload: dict = {
        'sub': user.username,
    }
    token = encode_jwt(payload)
    return Token(
        access_token=token,
        token_type='Bearer'
    )


@user_router.post('', response_model=UserRead)
async def register_user(
    uow: UOWDep,
    user_in: UserCreate
):
    return await UserService.register_user(uow, user_in)


@user_router.get('/me', response_model=UserRead)
async def get_me(
    current_user: UserRead = Depends(get_current_user)
) -> UserRead:
    return current_user
