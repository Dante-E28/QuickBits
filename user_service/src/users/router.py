import uuid
from fastapi import APIRouter, Depends, status

from src.users.services import AuthService, UserService
from src.users.dependencies import (
    UOWDep,
    get_current_user_for_refresh,
    get_verified_user,
    validate_auth_user
)
from src.users.schemas import Token, UserCreate, UserRead, UserUpdate


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
    return await UserService.edit_me(uow, user_update, current_user.id)


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
