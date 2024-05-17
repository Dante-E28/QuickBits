from src.config import settings


rabbit_url = (
    f'amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASS}@'
    f'{settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}/'
)

RABBIT_REPLY = "amq.rabbitmq.reply-to"

# Queue's name for request.
USER_SERVICE = 'user_service'
