from typing import Annotated

from fastapi import Depends

from src.schemas.comments import CommentsSchema
from src.schemas.posts import PostsSchema
from src.services.comments import CommentsService
from src.services.posts import PostsService
from src.unitofwork import IUnitOfWork, UnitOfWork


UOWDep = Annotated[IUnitOfWork, Depends(UnitOfWork)]


async def no_cache_get_comment(uow: UOWDep, comment_id: int) -> CommentsSchema:
    return await CommentsService.get_comment(uow, comment_id)


async def no_cache_get_post(uow: UOWDep, post_id: int) -> PostsSchema:
    return await PostsService.get_post(uow, post_id)
