from asyncio import Queue
import json
from typing import Any

from aio_pika import IncomingMessage, Message, connect_robust
from aio_pika.abc import (
    AbstractChannel,
    AbstractRobustConnection
)

from src.rabbitmq.rabbit_config import RABBIT_REPLY, USER_SERVICE, rabbit_url


class RabbitConnection:
    def __init__(self, url: str):
        self.url: str = url
        self.connection: AbstractRobustConnection | None = None
        self.channel: AbstractChannel | None = None

    async def connect(self):
        """Connect to RabbitMQ."""
        self.connection = await connect_robust(self.url)
        self.channel = await self.connection.channel()

    async def close(self):
        if self.connection and not self.connection.is_closed:
            await self.connection.close()


class DirectReplyClient:
    def __init__(self, channel: AbstractChannel | None):
        self.channel: AbstractChannel | None = channel

    @staticmethod
    def _serialize_json_message(
        payload: dict,
        reply_to: str,
        method_name: str
    ) -> Message:
        return Message(
            body=json.dumps(
                payload, ensure_ascii=False, default=repr).encode(),
            content_type='application/json',
            reply_to=reply_to,
            headers={'method_name': method_name}
        )

    @staticmethod
    def _deserialize_json_message(message: IncomingMessage) -> dict:
        return json.loads(message.body)

    async def publish(
        self,
        method_name: str,
        kwargs: dict[str, Any] | None = None
    ) -> dict:
        if not self.channel:
            return ValueError({'dfs'})
        callback_queue = await self.channel.declare_queue(RABBIT_REPLY)
        response_queue: Queue = Queue(maxsize=1)
        consumer_tag = await callback_queue.consume(
            callback=response_queue.put,
            no_ack=True
        )
        message = self._serialize_json_message(
            payload=kwargs or {},
            reply_to=RABBIT_REPLY,
            method_name=method_name
        )
        await self.channel.default_exchange.publish(
            message=message,
            routing_key=USER_SERVICE
        )
        response: IncomingMessage = await response_queue.get()

        await callback_queue.cancel(consumer_tag)
        return self._deserialize_json_message(response)


rabbit_connection = RabbitConnection(rabbit_url)
rabbit_client = DirectReplyClient(None)
