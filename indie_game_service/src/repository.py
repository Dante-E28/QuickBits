from src.database import new_session
from src.schemas.posts import PostsSchema
from src.models import Posts


class PostRepository:
    @classmethod
    async def add_post(cls, data: PostsSchema):
        async with new_session() as session:
            post_dict = data.model_dump()

            post = Posts(**post_dict)
            session.add(post)
            await session.commit()
            await session.refresh(post)
            return post
