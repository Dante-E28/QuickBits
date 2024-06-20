import uuid
from fastapi import APIRouter, status
from fastapi_cache.decorator import cache

from src.deps import UOWDep
from src.schemas.likes import LikesSchema, LikesSchemaAdd, LikesSchemaDelete
from src.services.likes import LikesService


router = APIRouter()


@router.get('', response_model=list[LikesSchema])
@cache(expire=15)
async def get_all_likes(uow: UOWDep, post_id: int) -> list[LikesSchema]:
    return await LikesService.get_likes(uow, post_id)


@router.get('/{post_id}', response_model=bool)
async def get_like(
    uow: UOWDep, post_id: int, user_id: uuid.UUID
) -> bool:
    return await LikesService.get_like(uow, post_id, user_id)


@router.post('', response_model=LikesSchema)
async def create_like(uow: UOWDep, like_in: LikesSchemaAdd) -> LikesSchema:
    return await LikesService.add_like(uow, like_in)


@router.delete('', status_code=status.HTTP_204_NO_CONTENT)
async def delete_like(
    uow: UOWDep,
    like: LikesSchemaDelete
) -> None:
    return await LikesService.delete_like(uow, like)
