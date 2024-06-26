import uuid
from fastapi import APIRouter, Query, status

from src.deps import UOWDep
from src.schemas.likes import LikesSchema, LikesSchemaAdd, LikesSchemaDelete
from src.services.likes import LikesService


router = APIRouter()


@router.get('/likes', response_model=list[int])
async def get_all_likes(
    uow: UOWDep,
    post_ids: list[int] = Query(default=None)
) -> list[int]:
    return await LikesService.get_likes_by_post_ids(uow, post_ids)


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
