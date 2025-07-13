from celery import Celery
from app.core.config import RABBITMQ_URL

app = Celery(
    "tasks",
    broker=RABBITMQ_URL,
    backend="rpc://"
)

app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'
app.conf.accept_content = ['json']
