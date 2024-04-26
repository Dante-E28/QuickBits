from pydantic import ValidationError
import pytest
from contextlib import nullcontext as does_not_raise

from src.services.comments import CommentsService
from src.services.likes import LikesService
from src.exceptions import EntityAlreadyExistsError, EntityNotFoundError
from src.schemas.posts import PostsSchemaAdd, PostsSchemaUpdate
from src.services.posts import PostsService


@pytest.mark.asyncio
class TestPostsService:
    @pytest.mark.parametrize(
        'name, description, expectation',
        [
            ['Гига', 'Амагама пиф паф', does_not_raise()],
            [None, 'Амагама пиф пуф', pytest.raises(ValidationError)],
            ['Гаген', None, pytest.raises(ValidationError)],
            [1, 'Все мы тут не в бытие', pytest.raises(ValidationError)],
            ['Сгусток слиси', 1, pytest.raises(ValidationError)],
            [None, None, pytest.raises(ValidationError)]
        ]
    )
    async def test_add_post(self, uow, name, description, expectation):
        with expectation:
            data = PostsSchemaAdd(
                name=name,
                user_id=1,
                description=description
            )
            post = await PostsService.add_post(uow, data)
            test_post = await PostsService.get_post(uow, post_id=post.id)
            assert test_post.name == data.name
            assert test_post.description == data.description

    async def test_add_duplicate_post(self, uow, posts):
        with pytest.raises(EntityAlreadyExistsError):
            data = PostsSchemaAdd(
                name='Гига',
                user_id=1,
                description='А когда не говно?'
            )
            await PostsService.add_post(uow, post=data)

    async def test_get_none_posts(self, uow):
        none_posts = await PostsService.get_posts(uow)
        assert none_posts == []

    async def test_get_posts(self, uow, posts):
        posts = await PostsService.get_posts(uow)
        assert posts is not None
        assert len(posts) == 2
        for post in posts:
            assert post.name in ['Гига', 'Гига СТЭС']
            assert post.description in ['Помпеи', 'Сморк']

    async def test_get_post(self, uow, posts):
        post = await PostsService.get_post(uow, post_id=1)
        assert post is not None
        assert post.name == 'Гига'
        assert post.description == 'Помпеи'

    @pytest.mark.parametrize(
        'name, description, expectation',
        [
            ['Супер игра три тыщы', 'Амагама пиф паф', does_not_raise()],
            [None, 'Амагама пиф пуф', does_not_raise()],
            ['Гаген', None, does_not_raise()],
            [1, 'Все мы тут не в бытие', pytest.raises(ValidationError)],
            ['Сгусток слиси', 1, pytest.raises(ValidationError)],
        ]
    )
    async def test_edit_post(self, uow, name, description, expectation, posts):
        with expectation:
            post = PostsSchemaUpdate(
                name=name,
                description=description
            )
            old_post = await PostsService.get_post(uow, post_id=1)
            await PostsService.edit_post(uow, update_post=post, post_id=1)
            new_post = await PostsService.get_post(uow, post_id=1)
            if post.name:
                assert new_post.name == post.name
            else:
                assert new_post.name == old_post.name
            if post.description:
                assert new_post.description == post.description
            else:
                assert new_post.description == old_post.description

    async def test_delete_post(self, uow, posts, comments, likes):
        await PostsService.delete_post(uow, post_id=1)
        with pytest.raises(EntityNotFoundError):
            await PostsService.get_post(uow, post_id=1)
            await CommentsService.get_comment(uow, comment_id=1)
            await LikesService.get_like(uow, post_id=1, user_id=2)
