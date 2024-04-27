from abc import ABC, abstractmethod

from src.database import new_session, engine
from src.model import Users
from src.repository import UsersRepository


class IUnitOfWork(ABC):
    users: UsersRepository

    @abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
        raise NotImplementedError

    @abstractmethod
    async def __aexit__(self, *args):
        raise NotImplementedError

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError


class UnitOfWork(IUnitOfWork):

    def __init__(self):
        self.session_factory = new_session

    async def __aenter__(self):
        self.session = self.session_factory()
        self.users = UsersRepository(Users, self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()