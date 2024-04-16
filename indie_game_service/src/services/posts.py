from fastapi import HTTPException, status
from sqlalchemy.exc import NoResultFound
from src.schemas.posts import PostsSchema, PostsSchemaAdd, PostsSchemaUpdate
from src.unitofwork import IUnitOfWork


class PostsService:

    @staticmethod
    async def add_post(
        uow: IUnitOfWork,
        post: PostsSchemaAdd
    ) -> PostsSchema:
        """Add post"""
        async with uow:
            result = await uow.posts.add(post.model_dump())
            await uow.commit()
            return PostsSchema.model_validate(result)

    @staticmethod
    async def get_posts(
        uow: IUnitOfWork
    ) -> list[PostsSchema]:
        """Get all posts"""
        async with uow:
            posts = await uow.posts.get_all()
            return [PostsSchema.model_validate(post) for post in posts]

    @staticmethod
    async def get_post(
        uow: IUnitOfWork,
        post_id: int
    ) -> PostsSchema:
        """Get post by id"""
        async with uow:
            try:
                post = await uow.posts.get(id=post_id)
            except NoResultFound:
                raise HTTPException(
                    status_code=404,
                    detail=f'Post id: {post_id} not found',
                )
            return PostsSchema.model_validate(post)

    @staticmethod
    async def edit_post(
        uow: IUnitOfWork,
        post_id: int,
        update_post: PostsSchemaUpdate
    ) -> PostsSchema:
        """Edit post"""
        async with uow:
            try:
                result = await uow.posts.update(
                    data=update_post.model_dump(
                        exclude_none=True), id=post_id
                    )
                await uow.commit()
                return PostsSchema.model_validate(result)
            except NoResultFound:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'Comment id: {post_id} not found'
                )

    @staticmethod
    async def delete_post(
        uow: IUnitOfWork,
        post_id: int
    ) -> None:
        """Delete post"""
        async with uow:
            exists_post = await PostsService.get_post(uow, post_id)
            if exists_post:
                await uow.posts.delete(id=post_id)
                await uow.commit()
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'Comment id: {post_id} not found'
                )
