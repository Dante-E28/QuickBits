from src.unitofwork import IUnitOfWork
from src.schema import UsersSchema, UsersSchemaAdd


class UsersService:

    @staticmethod
    async def add_user(
        uow: IUnitOfWork,
        user: UsersSchemaAdd
    ) -> UsersSchema:
        async with uow:
            result = await uow.users.add(user.model_dump())
            await uow.commit()
            return UsersSchema.model_validate(result)
