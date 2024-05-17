import aio_pika
from contextlib import asynccontextmanager

RABBITMQ_URL = "amqp://admin:admin@127.0.0.1:5672/"


class RabbitMQClient:
    def __init__(self, url: str):
        self.url = url
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.url)
        self.channel = await self.connection.channel()

    async def declare_queue(self, queue_name: str):
        return await self.channel.declare_queue(queue_name, durable=True)

    async def publish_message(self, message: str, queue_name: str):
        await self.channel.default_exchange.publish(
            aio_pika.Message(body=message.encode()),
            routing_key=queue_name,
        )

    async def consume_messages(self, queue_name: str, callback):
        queue = await self.declare_queue(queue_name)
        await queue.consume(callback)

    async def close(self):
        if self.connection:
            await self.connection.close()



@asynccontextmanager
async def get_rabbitmq_client():
    client = RabbitMQClient(RABBITMQ_URL)
    await client.connect()
    try:
        yield client
    finally:
        await client.close()
