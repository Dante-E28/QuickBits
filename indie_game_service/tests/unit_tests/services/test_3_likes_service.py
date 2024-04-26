import pytest
from contextlib import nullcontext as does_not_raise
from pydantic import ValidationError

from src.schemas.likes import LikesSchemaAdd, LikesSchemaDelete
from src.services.likes import LikesService
from src.exceptions import EntityNotFoundError


@pytest.mark.asyncio
class TestLikesService:
    @pytest.mark.parametrize(
        'post_id, expectation',
        [
            [1, does_not_raise()],
            [None, pytest.raises(ValidationError)],
            ['dsada', pytest.raises(ValidationError)],
            [10, pytest.raises(EntityNotFoundError)]
        ]
    )
    async def test_add_like(self, uow, post_id, expectation, posts):
        with expectation:
            data = LikesSchemaAdd(post_id=post_id, user_id=1)
            like = await LikesService.add_like(uow, like=data)
            assert like.post_id == data.post_id

    async def test_get_none_likes(self, uow, posts):
        none_likes = await LikesService.get_likes(uow, post_id=1)
        assert none_likes == []

    async def test_get_like(self, uow, posts, likes):
        like = await LikesService.get_like(uow, post_id=1, user_id=2)
        assert like is True

    async def test_delete_like(self, uow, posts, likes):
            like = LikesSchemaDelete(post_id=1, user_id=2)
            exists_like_before = await LikesService.get_like(
                uow, post_id=1, user_id=2
            )
            assert exists_like_before is not None
            await LikesService.delete_like(uow, like=like)
            exists_like_after = await LikesService.get_like(
                uow, post_id=1, user_id=2
            )
            assert exists_like_after is False
