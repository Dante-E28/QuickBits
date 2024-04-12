from src.models import Comments
from src.repository import SQLAlchemyRepository


class CommentsRepository(SQLAlchemyRepository[Comments]):
    pass
