from fastapi import APIRouter


router = APIRouter(prefix='/likes', tags=['Likes'])


@router.get('', response_model=None)
async def get_all_likes() -> None:
    return None


@router.post('', response_model=None)
async def create_like() -> None:
    return None


@router.delete('/{like_id}', response_model=None)
async def delete_like() -> None:
    return None
