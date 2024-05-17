import json
from typing import Any, Callable

from aio_pika import Message, connect_robust
from aio_pika.abc import (
    AbstractChannel,
    AbstractIncomingMessage,
    AbstractRobustConnection,
    AbstractQueue
)
from pydantic import BaseModel

from src.rabbitmq.rabbit_config import RABBITMQ_URL
from src.rabbitmq.functions_list import functions


class RabbitServer:
    def __init__(self) -> None:
        self.connection: AbstractRobustConnection | None = None
        self.channel: AbstractChannel | None = None
        self.queue: AbstractQueue | None = None
        self.queue_name: str = 'user_service'
        self.functions: dict = functions

    async def connect(self):
        self.connection = await connect_robust(url=RABBITMQ_URL)
        self.channel = await self.connection.channel()

    async def close_connection(self):
        if self.connection:
            if not self.connection.is_closed:
                await self.connection.close()

    async def initialize_consumer(self):
        """Initialize the consumer and start consuming messages."""
        if self.channel:
            self.queue = await self.channel.declare_queue(
                self.queue_name,
                auto_delete=True
            )
            await self.queue.consume(self.consumer)

    @classmethod
    async def create_server(cls) -> 'RabbitServer':
        """Create a server and return."""
        server = cls()
        await server.connect()
        await server.initialize_consumer()
        return server

    @staticmethod
    def _serialize_json_message(payload: dict) -> Message:
        return Message(
            body=json.dumps(
                payload, ensure_ascii=False, default=repr).encode(),
            content_type='application/json',
        )

    @staticmethod
    def _deserialize_json_message(message: AbstractIncomingMessage):
        return json.loads(message.body)

    @staticmethod
    async def _execute(func: Callable, payload: dict[str, Any]) -> Any:
        return await func(**payload)

    @staticmethod
    def _serialize_exception(exception: Exception) -> dict[str, dict]:
        return {
            'error': {
                'type': exception.__class__.__name__,
                'message': repr(exception),
                'args': exception.args
            }
        }

    async def get_result_from_function(self, func_name: str, payload: dict):
        """Execute function and return data."""
        try:
            func = functions[func_name]
            result = await self._execute(func, payload)
            if isinstance(result, BaseModel):
                result = result.model_dump()
        except Exception as e:
            result = self._serialize_exception(e)
        return result

    async def consumer(self, message: AbstractIncomingMessage):
        if not self.channel:
            return

        async with message.process():
            if message.reply_to:
                data_for_response = await self.get_result_from_function(
                    func_name=str(message.headers.get('method_name')),
                    payload=self._deserialize_json_message(message)
                )
                await self.channel.default_exchange.publish(
                    message=self._serialize_json_message(
                        data_for_response
                    ),
                    routing_key=message.reply_to
                )
