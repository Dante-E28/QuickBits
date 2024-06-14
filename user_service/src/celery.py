from celery import Celery

from src.rabbitmq.rabbit_config import RABBITMQ_URL


celery = Celery('user_service_tasks', broker=RABBITMQ_URL)

import src.emails.utils # noqa
