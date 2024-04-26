from pydantic import ValidationError
import pytest
from contextlib import nullcontext as does_not_raise

from src.exceptions import EntityNotFoundError
from src.schemas.comments import CommentsSchemaAdd, CommentsSchemaUpdate
from src.services.comments import CommentsService


@pytest.mark.asyncio
class TestCommentsSerivce:
    @pytest.mark.parametrize(
        'text, post_id, expectation',
        [
            ['Дизлайк + атписка', 2, does_not_raise()],
            [None, 1, pytest.raises(ValidationError)],
            ['Свинутс ты обосрався', None, pytest.raises(ValidationError)],
            ['Все мы тут лишние', 10, pytest.raises(EntityNotFoundError)]
        ]
    )
    async def test_add_comment(self, uow, text, post_id, expectation, posts):
        with expectation:
            data = CommentsSchemaAdd(user_id=1, text=text, post_id=post_id)
            comment = await CommentsService.add_comment(uow, comment=data)
            assert comment.text == data.text
            assert comment.post_id == data.post_id

    async def test_get_none_comments(self, uow, posts):
        none_comments = await CommentsService.get_comments(uow, post_id=1)
        assert none_comments == []

    async def test_get_comments(self, uow, posts, comments):
        comments = await CommentsService.get_comments(uow, post_id=1)
        assert comments is not None
        assert len(comments) == 2
        for comment in comments:
            assert comment.text in [
                'Божественный контент', 'Ну могло быть и лучше'
            ]

    async def test_get_comment(self, uow, posts, comments):
        comment = await CommentsService.get_comment(uow, comment_id=1)
        assert comment is not None
        assert comment.text == 'Божественный контент'
        assert comment.post_id == 1

    @pytest.mark.parametrize(
        'text, expectation',
        [
            ['Биба и боба', does_not_raise()],
            [1, pytest.raises(ValidationError)],
        ]
    )
    async def test_edit_comment(
        self, uow, text, expectation, posts, comments
    ):
        with expectation:
            comment = CommentsSchemaUpdate(text=text)
            old_comment = await CommentsService.get_comment(uow, comment_id=1)
            update_comment = await CommentsService.edit_comment(
                uow, comment_id=1, update_comment=comment
            )
            new_comment = await CommentsService.get_comment(uow, comment_id=1)
            if new_comment.text:
                assert new_comment.text == update_comment.text
            else:
                assert new_comment.text == old_comment.text
            if new_comment.post_id:
                assert new_comment.post_id == update_comment.post_id
            else:
                assert new_comment.post_id == old_comment.post_id

    async def test_delete_comment(self, uow, posts, comments):
        await CommentsService.delete_comment(uow, comment_id=1)
        with pytest.raises(EntityNotFoundError):
            await CommentsService.get_comment(uow, comment_id=1)
