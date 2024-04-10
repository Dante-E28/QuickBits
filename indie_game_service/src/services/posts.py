from src.database import new_session
from src.schemas.posts import PostsSchema
from src.models import Posts


class PostService:
    @staticmethod
    async def create(post: PostsSchema) -> Posts:
        """Create post"""
        async with new_session() as session:
            db_post = Posts(**post.model_dump())
            session.add(db_post)
            await session.commit()
            await session.refresh(db_post)
            return db_post
