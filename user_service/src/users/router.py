import uuid
from fastapi import APIRouter, Depends, Response, status

from src.config import settings
from src.constants import (
    ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE, SECONDS_IN_MINUTE)
from src.users.services import AuthService, UserService
from src.users.dependencies import (
    UOWDep,
    get_current_user,
    get_current_user_for_refresh,
    validate_auth_user
)
from src.users.schemas import Token, UserCreate, UserRead, UserUpdate
from src.users.utils import set_cookies


auth_router = APIRouter(prefix='/auth', tags=['Auth'])
user_router = APIRouter(prefix='/user', tags=['User'])

ACCESS_EXPIRE = settings.auth_settings.access_token_expire_minutes


@auth_router.post('/token', response_model=Token)
async def token(
    user: UserRead = Depends(validate_auth_user)
) -> Token:
    access_token = AuthService.create_access_token(user)
    refresh_token = AuthService.create_refresh_token(user)
    return Token(
        access_token=access_token,
        refresh_token=refresh_token
    )


@auth_router.post('/login', status_code=status.HTTP_200_OK)
async def login(
    response: Response,
    token: Token = Depends(token)
):
    set_cookies(
        response=response,
        access_token=token.access_token,
        refresh_token=token.refresh_token
    )
    response.status_code = status.HTTP_200_OK
    return {
        'message': 'You are logged in!',
        'expire': ACCESS_EXPIRE * SECONDS_IN_MINUTE
    }


@auth_router.post('/logout', status_code=status.HTTP_200_OK)
async def logout(
    response: Response
):
    response.delete_cookie(ACCESS_TOKEN_TYPE)
    response.delete_cookie(REFRESH_TOKEN_TYPE)
    return {'message': 'You are logged out!'}


@auth_router.post(
    '/refresh_token',
    response_model=Token,
    response_model_exclude_none=True
)
async def refresh_token(
    user: UserRead = Depends(get_current_user_for_refresh)
):
    access_token = AuthService.create_access_token(user)
    return Token(
        access_token=access_token
    )


@auth_router.post('/refresh')
async def refresh(
    response: Response,
    token: Token = Depends(refresh_token)
):
    set_cookies(response=response, access_token=token.access_token)
    return {
        'message': 'Token refreshed!',
        'expire': ACCESS_EXPIRE * SECONDS_IN_MINUTE
    }


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


@user_router.get('', response_model=list[UserRead])
async def get_all_users(uow: UOWDep) -> list[UserRead]:
    return await UserService.get_users(uow)


@user_router.get('/{user_id}', response_model=UserRead)
async def get_user(uow: UOWDep, user_id: uuid.UUID):
    return await UserService.get_user(uow, user_id)


@user_router.patch('/me', response_model=UserUpdate)
async def update_me(
    uow: UOWDep,
    user_update: UserUpdate,
    current_user: UserRead = Depends(get_me)
) -> UserRead:
    return await UserService.edit_user(uow, user_update, current_user.id)


@user_router.patch('/{user_id}', response_model=UserUpdate)
async def update_user(
    uow: UOWDep,
    user_update: UserUpdate,
    user: UserRead = Depends(get_user)
) -> UserRead:
    return await UserService.edit_user(uow, user_update, user.id)


@user_router.delete('/me', status_code=status.HTTP_204_NO_CONTENT)
async def delete_me(
    uow: UOWDep,
    current_user: UserRead = Depends(get_me)
) -> None:
    await UserService.delete_me(uow, current_user.id)


@user_router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    uow: UOWDep,
    user: UserRead = Depends(get_user)
) -> None:
    await UserService.delete_user(uow, user.id)
