from sqlalchemy.exc import NoResultFound

from src.schemas.likes import LikesSchema, LikesSchemaAdd
from src.unitofwork import IUnitOfWork


class LikesService:

    @staticmethod
    async def add_or_delete_like(
        uow: IUnitOfWork,
        like: LikesSchemaAdd
    ) -> LikesSchema:
        async with uow:
            try:
                existing_like = await uow.likes.get(
                    user_id=like.user_id, post_id=like.post_id
                )
            except NoResultFound:
                existing_like = None
            if existing_like is not None:
                result = await uow.likes.delete(
                    user_id=like.user_id, post_id=like.post_id
                )
            else:
                result = await uow.likes.add(like.model_dump())
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

    #@staticmethod
    #async def delete_like(
        #uow: IUnitOfWork,
        #like_id: int
    #) -> None:
        #async with uow:
            #await uow.likes.delete(id=like_id)
            #await uow.commit()
