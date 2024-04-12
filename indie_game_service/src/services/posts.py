from typing import Dict, List

from src.unitofwork import IUnitOfWork
from src.schemas.posts import PostsSchema, PostsSchemaAdd


class PostService:

    @staticmethod
    async def add_post(uow: IUnitOfWork, post: PostsSchemaAdd) -> PostsSchema:
        """Add post"""
        async with uow:
            result = await uow.posts.add(post.model_dump())
            await uow.commit()
            return PostsSchema.model_validate(result)

    @staticmethod
    async def get_posts(uow: IUnitOfWork) -> List[PostsSchema]:
        """Get all posts"""
        async with uow:
            posts = await uow.posts.get_all()
            return [PostsSchema.model_validate(post) for post in posts]

    @staticmethod
    async def get_post(uow: IUnitOfWork, post_id: int) -> PostsSchema:
        """Get post by id"""
        async with uow:
            post = await uow.posts.get(id=post_id)
            return PostsSchema.model_validate(post)

    @staticmethod
    async def edit_post(
        uow: IUnitOfWork,
        post_id: int,
        post_data: Dict
    ) -> PostsSchema:
        """Edit post"""
        async with uow:
            updated_post = PostsSchemaAdd.model_validate(post_data)
            post = await uow.posts.update(
                id=post_id,
                data=updated_post.model_dump())
            await uow.commit()
            return PostsSchema.model_validate(post)

    @staticmethod
    async def delete_post(uow: IUnitOfWork, post_id: int) -> PostsSchema:
        """Delete post"""
        async with uow:
            post = await uow.posts.delete(id=post_id)
            await uow.commit()
            return PostsSchema.model_validate(post)
