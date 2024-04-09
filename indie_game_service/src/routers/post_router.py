from fastapi import APIRouter

router = APIRouter(prefix='/post', tags=['Post'])


@router.get('', response_model=None)
async def get_all_posts() -> int:
    return 'sdf'


@router.get('/{post_id}', response_model=None)
