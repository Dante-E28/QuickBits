from sqlalchemy.exc import IntegrityError
from src.exceptions import EntityNotFoundError, EntityAlreadyExistsError
from src.schemas.likes import LikesSchema, LikesSchemaAdd, LikesSchemaDelete
from src.unitofwork import IUnitOfWork


class LikesService:

    @staticmethod
    async def add_like(
        uow: IUnitOfWork,
        like: LikesSchemaAdd
    ) -> LikesSchema:
        async with uow:
            exists_like = await LikesService.get_like(
                uow, like.post_id, like.user_id
            )
            if not exists_like:
                try:
                    result = await uow.likes.add(like.model_dump())
                    await uow.commit()
                    return LikesSchema.model_validate(result)
                except IntegrityError:
                    raise EntityNotFoundError('Post', like.post_id)
            else:
                raise EntityAlreadyExistsError('Like')

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
            result = await uow.likes.get(post_id=post_id, user_id=user_id)
            if result:
                return True
            else:
                return False

    @staticmethod
    async def delete_like(
        uow: IUnitOfWork,
        like: LikesSchemaDelete
    ) -> None:
        async with uow:
            exists_like = await LikesService.get_like(
                uow, like.post_id, like.user_id
            )
            if exists_like:
                await uow.likes.delete(
                    user_id=like.user_id, post_id=like.post_id
                )
                await uow.commit()
            else:
                raise EntityNotFoundError('Post', like.post_id)
