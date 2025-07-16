import asyncio
import json
from uuid import UUID

import aio_pika
from app.core.celery_app import app
from app.core.config import RABBITMQ_URL


async def publish_message(message: dict):
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    await channel.default_exchange.publish(
        aio_pika.Message(body=json.dumps(message).encode()), routing_key="telegram_queue"
    )
    await connection.close()


@app.task
def schedule_telegram_message(chat_id: int, text: str, reg_id: UUID):
    asyncio.run(publish_message({"chat_id": chat_id, "text": text, "reg_id": str(reg_id)}))


@app.task
def schedule_telegram_qr(chat_id: int, text: str, reg_id: UUID, data: str):
    asyncio.run(publish_message({"chat_id": chat_id, "text": text, "reg_id": str(reg_id), "data": data}))
