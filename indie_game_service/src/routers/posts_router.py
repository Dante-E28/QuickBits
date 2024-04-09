from fastapi import APIRouter

router = APIRouter(prefix='/posts', tags=['Posts'])


@router.get('', response_model=None)
async def get_all_posts() -> None:
    return None


@router.get('/{post_id}', response_model=None)
async def get_post() -> None:
    return None


@router.post('', response_model=None)
async def create_post() -> None:
    return None


@router.patch('/{post_id}', response_model=None)
async def update_post() -> None:
    return None


@router.delete('/{post_id}', response_model=None)
async def delete_post() -> None:
    return None
