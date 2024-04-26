from src.exceptions import EntityAlreadyExistsError, EntityNotFoundError
from src.schemas.posts import PostsSchema, PostsSchemaAdd, PostsSchemaUpdate
from src.unitofwork import IUnitOfWork
from sqlalchemy.exc import IntegrityError

class PostsService:

    @staticmethod
    async def add_post(
        uow: IUnitOfWork,
        post: PostsSchemaAdd
    ) -> PostsSchema:
        """Add post"""
        async with uow:
            try:
                result = await uow.posts.add(post.model_dump())
                await uow.commit()
                return PostsSchema.model_validate(result)
            except IntegrityError:
                raise EntityAlreadyExistsError('Post')

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
            result = await uow.posts.get(id=post_id)
            if result:
                return PostsSchema.model_validate(result)
            else:
                raise EntityNotFoundError('Post', post_id)

    @staticmethod
    async def edit_post(
        uow: IUnitOfWork,
        update_post: PostsSchemaUpdate,
        post_id: int,
    ) -> PostsSchema:
        """Edit post"""
        async with uow:
            result = await uow.posts.update(
                data=update_post.model_dump(exclude_none=True),
                id=post_id
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
