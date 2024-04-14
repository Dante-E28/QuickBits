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
            result = await uow.comments.add(comment.model_dump())
            await uow.commit()
            return CommentsSchema.model_validate(result)

    @staticmethod
    async def get_comments_for_post(
        uow: IUnitOfWork,
        post_id: int,
    ) -> list[CommentsSchema]:
        """Get comments on the post"""
        async with uow:
            comms = await uow.comments.get_all(post_id=post_id)
            return [CommentsSchema.model_validate(comm) for comm in comms]

    @staticmethod
    async def get_post_for_comment(
        uow: IUnitOfWork,
        comment_id: int,
    ) -> CommentsSchema:
        """Get post for comment id"""
        async with uow:
            result = await uow.comments.get(id=comment_id)
            return CommentsSchema.model_validate(result)

    @staticmethod
    async def edit_comment(
        uow: IUnitOfWork,
        comment_id: int,
        update_comment: CommentsSchemaUpdate
    ) -> CommentsSchema:
        """Edit comment"""
        async with uow:
            comment = await uow.comments.update(
                data=update_comment.model_dump(), id=comment_id
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
