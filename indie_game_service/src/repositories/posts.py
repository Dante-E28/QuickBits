from src.models import Posts
from src.repository import SQLAlchemyRepository


class PostsRepository(SQLAlchemyRepository[Posts]):
    pass
