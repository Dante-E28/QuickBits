

from typing import List
from src.schemas.likes import LikesSchema, LikesSchemaAdd
from src.unitofwork import IUnitOfWork


class LikesService:

    @staticmethod
    async def add_like(
        uow: IUnitOfWork,
        like: LikesSchemaAdd
    ) -> LikesSchema:
        async with uow:
            result = await uow.likes.add(like.model_dump())
            await uow.commit()
            return LikesSchema.model_validate(result)

    @staticmethod
    async def get_likes_for_post(
        uow: IUnitOfWork,
        post_id: int
    ) -> List[LikesSchema]:
        async with uow:
            likes = await uow.likes.get_all(post_id=post_id)
            return [LikesSchema.model_validate(like) for like in likes]

    @staticmethod
    async def delete_like(
        uow: IUnitOfWork,
        like_id: int
    ) -> None:
        async with uow:
            await uow.likes.delete(id=like_id)
            await uow.commit()
