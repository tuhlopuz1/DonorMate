import asyncio
import json
import logging
from uuid import UUID

import aio_pika
from aiogram.types import BotCommand
from core.config import RABBITMQ_URL
from core.dispatcher import bot, dp, send_message, send_qr
from dependencies.api_dependencies import check_notifications

logger = logging.getLogger(__name__)


async def on_message(message: aio_pika.IncomingMessage):
    async with message.process():
        data = json.loads(message.body)
        chat_id = data["chat_id"]
        text = data["text"]
        reg_id = data.get("reg_id")
        if reg_id:
            send = await check_notifications(chat_id=chat_id, reg_id=UUID(reg_id))
            if send:
                if data["data"]:
                    await send_qr(chat_id=chat_id, text=text, data=data["data"])
                else:
                    await send_message(chat_id, text)
        else:
            await send_message(chat_id, text)


async def connect_with_retry(url, retries=10, delay=5):
    for attempt in range(1, retries + 1):
        try:
            logger.info(f"Connecting to RabbitMQ (attempt {attempt})...")
            return await aio_pika.connect_robust(url)
        except Exception as e:
            logger.warning(f"Attempt {attempt} failed: {e}")
            await asyncio.sleep(delay)
    raise RuntimeError("Could not connect to RabbitMQ after retries")


async def start_rabbitmq_listener():
    connection = await connect_with_retry(RABBITMQ_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue("telegram_queue", durable=True)
    await queue.consume(on_message)
    logger.info("[*] Waiting for messages")


async def start_bot():
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Запустить мини-приложение"),
        ]
    )
    logger.info("Starting bot polling")
    await dp.start_polling(bot)


async def main():
    asyncio.create_task(start_rabbitmq_listener())
    await start_bot()


if __name__ == "__main__":
    asyncio.run(main())
