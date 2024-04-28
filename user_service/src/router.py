from fastapi import APIRouter, Depends

from src.services import AuthService
from src.dependencies import UOWDep, get_current_user_for_refresh, get_verified_user, validate_auth_user
from src.fake_service import UserService
from src.schemas import Token, UserCreate, UserRead


auth_router = APIRouter(prefix='/auth', tags=['Auth'])
user_router = APIRouter(prefix='/user', tags=['User'])


@auth_router.post('/login', response_model=Token)
async def login(
    user: UserRead = Depends(validate_auth_user)
):
    access_token = AuthService.create_access_token(user)
    refresh_token = AuthService.create_refresh_token(user)
    return Token(
        access_token=access_token,
        refresh_token=refresh_token
    )


@auth_router.post(
    '/refresh',
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


@user_router.post('', response_model=UserRead)
async def register_user(
    uow: UOWDep,
    user_in: UserCreate
):
    return await UserService.register_user(uow, user_in)


@user_router.get('/me', response_model=UserRead)
async def get_me(
    current_user: UserRead = Depends(get_verified_user)
) -> UserRead:
    return current_user
