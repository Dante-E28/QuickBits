from fastapi import HTTPException, status
from sqlalchemy.exc import NoResultFound
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
            try:
                await uow.posts.get(id=comment.post_id)
            except NoResultFound:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'Post id: {comment.post_id} not found'
                )
            result = await uow.comments.add(comment.model_dump())
            await uow.commit()
            return CommentsSchema.model_validate(result)

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
            try:
                result = await uow.comments.get(id=comment_id)
            except NoResultFound:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f'comment_id: {comment_id} not found',
                )
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
                data=update_comment.model_dump(
                    exclude_none=True), id=comment_id
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
