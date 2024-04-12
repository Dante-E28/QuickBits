from src.models import Likes
from src.repository import SQLAlchemyRepository


class LikesRepository(SQLAlchemyRepository[Likes]):
    pass