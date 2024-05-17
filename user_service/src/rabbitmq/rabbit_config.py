from src.config import settings


RABBITMQ_URL = (
    f'amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASS}@'
    f'{settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}/'
)
