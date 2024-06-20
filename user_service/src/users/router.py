import uuid

from fastapi import APIRouter, Depends, Response, status
from fastapi_cache.decorator import cache

from src.config import settings
from src.constants import (
    ACCESS_TOKEN_TYPE, EXPIRE, MESSAGE, REFRESH_TOKEN_TYPE, SECONDS_IN_MINUTE)
from src.emails.utils import send_reset_email, send_verify_email
from src.messages import (
    EMAIL_SEND, EMAIL_VERIFIED, LOGGED_IN, LOGGED_OUT, PASSWORD_RESET,
    TOKEN_REFRESHED
)
from src.users.services import AuthService, UserService
from src.users.dependencies import (
    UOWDep,
    get_current_user,
    get_current_user_for_refresh,
    get_reset_password_user,
    no_cache_get_user,
    validate_auth_user,
    validate_user_email,
    verify_current_user
)
from src.users.schemas import (
    PasswordReset, Token, UserCreate, UserRead, UserUpdate)
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
        MESSAGE: LOGGED_IN,
        EXPIRE: ACCESS_EXPIRE * SECONDS_IN_MINUTE
    }


@auth_router.post('/logout', status_code=status.HTTP_200_OK)
async def logout(
    response: Response
):
    response.delete_cookie(ACCESS_TOKEN_TYPE)
    response.delete_cookie(REFRESH_TOKEN_TYPE)
    return {MESSAGE: LOGGED_OUT}


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
        MESSAGE: TOKEN_REFRESHED,
        EXPIRE: ACCESS_EXPIRE * SECONDS_IN_MINUTE
    }


@auth_router.post('/email_verification')
async def send_verification(
    user: UserRead = Depends(get_current_user)
):
    token: str = AuthService.create_email_verification_token(user)
    send_verify_email(user.email, token)
    return {MESSAGE: EMAIL_SEND}


@auth_router.post('/email_verification/{token}')
async def verify_me(
    user: UserRead = Depends(verify_current_user)
):
    return {MESSAGE: EMAIL_VERIFIED}


@auth_router.post('/reset_password')
async def send_reset(
    user: UserRead | None = Depends(validate_user_email)
):
    if user:
        reset_token: str = AuthService.create_password_reset_token(user)
        send_reset_email(user.email, reset_token)
    return {MESSAGE: EMAIL_SEND}


@auth_router.post('/reset_password/{token}')
async def reset_password(
    uow: UOWDep,
    password_in: PasswordReset,
    user: UserRead = Depends(get_reset_password_user)
):
    await UserService.reset_password(uow, user.id, password_in)
    return {MESSAGE: PASSWORD_RESET}


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
@cache(expire=120)
async def get_all_users(uow: UOWDep) -> list[UserRead]:
    return await UserService.get_users(uow)


@user_router.get('/{user_id}', response_model=UserRead)
@cache(expire=120)
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
    user: UserRead = Depends(no_cache_get_user)
) -> UserRead:
    return await UserService.edit_user(uow, user_update, user.id)
