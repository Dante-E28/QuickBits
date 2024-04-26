from src.exceptions import EntityNotFoundError
from src.schemas.comments import (
    CommentsSchema, CommentsSchemaAdd,
    CommentsSchemaUpdate
)
from src.unitofwork import IUnitOfWork


class CommentsService:

    @staticmethod
    async def add_comment(
        uow: IUnitOfWork,
        comment: CommentsSchemaAdd
    ) -> CommentsSchema:
        """Add comment"""
        async with uow:
            exists_post = await uow.posts.get(id=comment.post_id)
            if exists_post:
                result = await uow.comments.add(comment.model_dump())
                await uow.commit()
                return CommentsSchema.model_validate(result)
            else:
                raise EntityNotFoundError('Post', comment.post_id)

    @staticmethod
    async def get_comments(
        uow: IUnitOfWork,
        post_id: int,
    ) -> list[CommentsSchema]:
        """Get comments on the post"""
        async with uow:
            comms = await uow.comments.get_all(post_id=post_id)
            return [CommentsSchema.model_validate(comm) for comm in comms]

    @staticmethod
    async def get_comment(
        uow: IUnitOfWork,
        comment_id: int,
    ) -> CommentsSchema:
        """Get comment for comment id"""
        async with uow:
            result = await uow.comments.get(id=comment_id)
            if result:
                return CommentsSchema.model_validate(result)
            else:
                raise EntityNotFoundError('Comment', comment_id)

    @staticmethod
    async def edit_comment(
        uow: IUnitOfWork,
        comment_id: int,
        update_comment: CommentsSchemaUpdate
    ) -> CommentsSchema:
        """Edit comment"""
        async with uow:
            comment = await uow.comments.update(
                data=update_comment.model_dump(exclude_none=True),
                id=comment_id
            )
            await uow.commit()
            return CommentsSchema.model_validate(comment)

    @staticmethod
    async def delete_comment(
        uow: IUnitOfWork,
        comment_id: int
    ) -> None:
        """Delete comment"""
        async with uow:
            await uow.comments.delete(id=comment_id)
            await uow.commit()
