import pytest

from src.services.likes import LikesService
from src.services.comments import CommentsService
from src.schemas.likes import LikesSchemaAdd
from src.schemas.comments import CommentsSchemaAdd
from src.schemas.posts import PostsSchemaAdd
from src.services.posts import PostsService


@pytest.fixture
async def posts(uow):
    post_1 = PostsSchemaAdd(name='Гига', user_id=1, description='Помпеи')
    post_2 = PostsSchemaAdd(name='Гига СТЭС', user_id=1, description='Сморк')
    await PostsService.add_post(uow, post=post_1)
    await PostsService.add_post(uow, post=post_2)
    await uow.commit()


@pytest.fixture
async def comments(uow):
    comment_1 = CommentsSchemaAdd(
        user_id=1,
        text='Божественный контент',
        post_id=1
    )
    comment_2 = CommentsSchemaAdd(
        user_id=3,
        text='Ну могло быть и лучше',
        post_id=1
    )
    comment_3 = CommentsSchemaAdd(
        user_id=2,
        text='богохульный контент',
        post_id=2
    )
    await CommentsService.add_comment(uow, comment=comment_1)
    await CommentsService.add_comment(uow, comment=comment_2)
    await CommentsService.add_comment(uow, comment=comment_3)
    await uow.commit()


@pytest.fixture
async def likes(uow):
    like_1 = LikesSchemaAdd(post_id=1, user_id=2)
    like_2 = LikesSchemaAdd(post_id=2, user_id=3)
    await LikesService.add_like(uow, like=like_1)
    await LikesService.add_like(uow, like=like_2)
    await uow.commit()
