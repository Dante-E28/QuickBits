from fastapi import APIRouter


router = APIRouter(prefix='/comments', tags=['Comments'])


@router.get('', response_model=None)
async def get_all_comments() -> None:
    return None


@router.get('/{comment_id}', response_model=None)
async def get_post() -> None:
    return None


@router.post('', response_model=None)
async def create_comment() -> None:
    return None


@router.patch('/{comment_id}', response_model=None)
async def update_comment() -> None:
    return None


@router.delete('/{comment_id}', response_model=None)
async def delete_comment() -> None:
    return None
