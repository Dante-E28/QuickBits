from fastapi import APIRouter, Depends, status
from fastapi_cache.decorator import cache

from src.deps import UOWDep, no_cache_get_post
from src.schemas.posts import PostsSchema, PostsSchemaAdd, PostsSchemaUpdate
from src.security.dependencies import get_common_permission
from src.services.posts import PostsService

router = APIRouter()


@router.get('', response_model=list[PostsSchema])
@cache(expire=60)
async def get_all_posts(uow: UOWDep) -> list[PostsSchema]:
    return await PostsService.get_posts(uow)


@router.get('/{post_id}', response_model=PostsSchema)
@cache(expire=60)
async def get_post(uow: UOWDep, post_id: int) -> PostsSchema:
    return await PostsService.get_post(uow, post_id)


@router.post(
    '',
    response_model=PostsSchema,
    dependencies=[Depends(get_common_permission)]
)
async def create_post(uow: UOWDep, post_in: PostsSchemaAdd) -> PostsSchema:
    return await PostsService.add_post(uow, post_in)


@router.patch(
    '/{post_id}',
    response_model=PostsSchema,
    dependencies=[Depends(get_common_permission)]
)
async def update_post(
    uow: UOWDep,
    post_update: PostsSchemaUpdate,
    post: PostsSchema = Depends(no_cache_get_post)
) -> PostsSchema:
    return await PostsService.edit_post(uow, post_update, post.id)


@router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    uow: UOWDep,
    post: PostsSchema = Depends(no_cache_get_post)
) -> None:
    return await PostsService.delete_post(uow, post.id)
