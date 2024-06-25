from fastapi import APIRouter, Depends, status
from fastapi_cache.decorator import cache

from src.deps import UOWDep, no_cache_get_comment
from src.redis_cache import clear_cache
from src.schemas.comments import (
    CommentsSchema,
    CommentsSchemaAdd,
    CommentsSchemaUpdate
)
from src.services.comments import CommentsService
from src.security.dependencies import get_common_permission


router = APIRouter()


@router.get('', response_model=list[CommentsSchema])
@cache(expire=30, namespace='all_comments')
async def get_all_comments_for_post(
    uow: UOWDep,
    post_id: int
) -> list[CommentsSchema]:
    return await CommentsService.get_comments(uow, post_id)


@router.get('/{comment_id}', response_model=CommentsSchema)
async def get_comment(uow: UOWDep, comment_id: int) -> CommentsSchema:
    return await CommentsService.get_comment(uow, comment_id)


@router.post('', response_model=CommentsSchema)
async def create_comment(
    uow: UOWDep,
    comment_in: CommentsSchemaAdd
) -> CommentsSchema:
    await clear_cache(
        get_all_comments_for_post,
        'all_comments',
        kwargs={'post_id': comment_in.post_id}
    )
    return await CommentsService.add_comment(uow, comment_in)


@router.patch(
    '/{comment_id}',
    response_model=CommentsSchema,
    dependencies=[Depends(get_common_permission)]
)
async def update_comment(
    uow: UOWDep,
    comment_update: CommentsSchemaUpdate,
    comment: CommentsSchema = Depends(no_cache_get_comment)
) -> CommentsSchema:
    await clear_cache(
        get_all_comments_for_post,
        'all_comments',
        kwargs={'post_id': comment.post_id}
    )
    return await CommentsService.edit_comment(uow, comment.id, comment_update)


@router.delete(
    '/{comment_id}',
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_comment(
    uow: UOWDep,
    comment: CommentsSchema = Depends(no_cache_get_comment)
) -> None:
    await clear_cache(
        get_all_comments_for_post,
        'all_comments',
        kwargs={'post_id': comment.post_id}
    )
    await CommentsService.delete_comment(uow, comment.id)
