from fastapi import APIRouter, status

from src.deps import UOWDep
from src.schemas.likes import LikesSchema, LikesSchemaAdd, LikesSchemaDelete
from src.services.likes import LikesService


router = APIRouter()


@router.get('', response_model=list[LikesSchema])
async def get_all_likes(uow: UOWDep, post_id: int) -> list[LikesSchema]:
    return await LikesService.get_likes_for_post(uow, post_id)


@router.post('', response_model=LikesSchema)
async def create_like(uow: UOWDep, like_in: LikesSchemaAdd) -> LikesSchema:
    return await LikesService.add_like(uow, like_in)


@router.delete('/{like_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_like(uow: UOWDep, like_delete: LikesSchemaDelete) -> None:
    return await LikesService.delete_like(uow, like_delete)
