from abc import ABC, abstractmethod
from typing import Any, Generic, Sequence, Type, TypeVar

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Model
from src.users.model import Users


class AbstractRepository(ABC):

    @abstractmethod
    async def add(self, data: Any):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def update(self, data: Any, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def get(self, **kwargs):
        raise NotImplementedError


ModelType = TypeVar('ModelType', bound=Model)


class SQLAlchemyRepository(AbstractRepository, Generic[ModelType]):

    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session: AsyncSession = session

    async def add(self, data: dict[str, Any]) -> ModelType:
        """Create a new entity."""
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def get(self, **filters) -> ModelType | None:
        """Gets a entity by filter."""
        stmt = select(self.model).filter_by(**filters)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

    async def get_all(self, **filters) -> Sequence[ModelType]:
        """Gets all entities or by filter."""
        stmt = select(self.model)
        if filters:
            stmt = stmt.filter_by(**filters)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    async def delete(self, **filters) -> ModelType | None:
        """Delete an existing entity."""
        stmt = select(self.model).filter_by(**filters)
        res = await self.session.scalar(stmt)
        await self.session.delete(res)
        return res

    async def update(self, data: dict[str, Any], **filters) -> ModelType:
        """Update an existing entity."""
        stmt = update(self.model).values(**data).filter_by(
            **filters).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()


class UsersRepository(SQLAlchemyRepository[Users]):
    pass
