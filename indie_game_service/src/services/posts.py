from src.unitofwork import IUnitOfWork
from src.schemas.posts import PostsSchema, PostsSchemaAdd, PostsSchemaUpdate


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
            ids = await uow.posts.get_all()
            if post_id not in ids:
                raise ValueError(f'Post {post_id} not found')
            post = await uow.posts.get(id=post_id)
            return PostsSchema.model_validate(post)

    @staticmethod
    async def edit_post(
        uow: IUnitOfWork,
        post_id: int,
        update_post: PostsSchemaUpdate
    ) -> PostsSchema:
        """Edit post"""
        async with uow:
            result = await uow.posts.update(
                data=update_post.model_dump(), id=post_id
            )
            await uow.commit()
            return PostsSchema.model_validate(result)

    @staticmethod
    async def delete_post(
        uow: IUnitOfWork,
        post_id: int
    ) -> None:
        """Delete post"""
        async with uow:
            await uow.posts.delete(id=post_id)
            await uow.commit()
