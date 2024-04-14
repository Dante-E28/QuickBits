from fastapi import APIRouter, Depends, status

from src.deps import UOWDep
from src.schemas.posts import PostsSchema, PostsSchemaAdd, PostsSchemaUpdate
from src.services.posts import PostService

router = APIRouter()


@router.get('', response_model=list[PostsSchema])
async def get_all_posts(uow: UOWDep) -> list[PostsSchema]:
    return await PostService.get_posts(uow)


@router.get('/{post_id}', response_model=PostsSchema)
async def get_post(uow: UOWDep, post_id: int) -> PostsSchema:
    return await PostService.get_post(uow, post_id)


@router.post('', response_model=PostsSchema)
async def create_post(uow: UOWDep, post_in: PostsSchemaAdd) -> PostsSchema:
    return await PostService.add_post(uow, post_in)


@router.patch('/{post_id}', response_model=PostsSchema)
async def update_post(
    uow: UOWDep,
    post_update: PostsSchemaUpdate,
    post: PostsSchema = Depends(get_post)
) -> PostsSchema:
    return await PostService.edit_post(uow, post.id, post_update)


@router.delete('/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    uow: UOWDep,
    post: PostsSchema = Depends(get_post)
) -> None:
    return await PostService.delete_post(uow, post.id)
