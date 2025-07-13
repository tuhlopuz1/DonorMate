from app.core.celery_app import app
import asyncio
import aio_pika
import json
import os

RABBITMQ_URL = os.environ.get("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")


async def publish_message(message: dict):
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    await channel.default_exchange.publish(
        aio_pika.Message(body=json.dumps(message).encode()),
        routing_key="telegram_queue"
    )
    await connection.close()


@app.task
def schedule_telegram_message(chat_id: int, text: str):
    asyncio.run(publish_message({"chat_id": chat_id, "text": text}))
