from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError, NoResultFound

from src.schemas.likes import LikesSchema, LikesSchemaAdd
from src.unitofwork import IUnitOfWork


class LikesService:

    @staticmethod
    async def add_like(
        uow: IUnitOfWork,
        like: LikesSchemaAdd
    ) -> LikesSchema:
        async with uow:
            existing_like = await LikesService.get_like(
                uow, like.post_id, like.user_id
            )
            if existing_like:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail='Like already exists'
                )
            try:
                result = await uow.likes.add(like.model_dump())
            except IntegrityError:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f'Post id: {like.post_id} not found'
                )
            await uow.commit()
            return LikesSchema.model_validate(result)

    @staticmethod
    async def get_likes_for_post(
        uow: IUnitOfWork,
        post_id: int
    ) -> list[LikesSchema]:
        async with uow:
            likes = await uow.likes.get_all(post_id=post_id)
            return [LikesSchema.model_validate(like) for like in likes]

    @staticmethod
    async def get_like(
        uow: IUnitOfWork,
        post_id: int,
        user_id: int
    ) -> bool:
        async with uow:
            try:
                await uow.likes.get(post_id=post_id, user_id=user_id)
                return True
            except NoResultFound:
                raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail='Like not found'
                    )

    @staticmethod
    async def delete_like(
        uow: IUnitOfWork,
        post_id: int,
        user_id: int
    ) -> None:
        async with uow:
            existing_like = await LikesService.get_like(
                uow, post_id, user_id
            )
            if existing_like:
                await uow.likes.delete(user_id=user_id, post_id=post_id)
                await uow.commit()
            else:
                raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail='Like not found'
                    )
