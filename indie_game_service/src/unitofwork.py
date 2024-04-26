from abc import ABC, abstractmethod

from src.database import new_session, engine
from src.models import Posts, Comments, Likes
from src.repositories.posts import PostsRepository
from src.repositories.comments import CommentsRepository
from src.repositories.likes import LikesRepository


class IUnitOfWork(ABC):
    posts: PostsRepository
    comments: CommentsRepository
    likes: LikesRepository

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

        self.posts = PostsRepository(Posts, self.session)
        self.comments = CommentsRepository(Comments, self.session)
        self.likes = LikesRepository(Likes, self.session)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
