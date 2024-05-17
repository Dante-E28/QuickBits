import uuid

from fastapi import APIRouter

from src.rabbitmq.client import rabbit_client


router = APIRouter(prefix='/rabbitmq', tags=['Rabbit'])


@router.get('/user/{user_id}')
async def get_user(user_id: uuid.UUID):
    payload: dict = {'user_id': user_id.hex}
    # result = await rpc_client.call('get_user', payload)
    result = await rabbit_client.publish('get_user', payload)
    return result
