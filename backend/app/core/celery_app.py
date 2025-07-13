from app.core.config import RABBITMQ_URL
from celery import Celery

app = Celery("tasks", broker=RABBITMQ_URL, backend="rpc://")

app.conf.task_serializer = "json"
app.conf.result_serializer = "json"
app.conf.accept_content = ["json"]

app.autodiscover_tasks(packages=["app.api.events"])
