import asyncio
import logging
import aio_pika
import json
from core.dispatcher import dp, bot, send_message
from core.config import RABBITMQ_URL
from aiogram.types import BotCommand

logger = logging.getLogger(__name__)


async def on_message(message: aio_pika.IncomingMessage):
    async with message.process():
        data = json.loads(message.body)
        chat_id = data["chat_id"]
        text = data["text"]
        await send_message(chat_id, text)


async def start_rabbitmq_listener():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue("telegram_queue", durable=True)
    await queue.consume(on_message)
    logger.info("[*] Waiting for messages")


async def start_bot():
    await bot.set_my_commands([
        BotCommand(command="start", description="Запустить мини-приложение")
    ])
    logger.info("Starting bot polling")
    await dp.start_polling(bot)


async def main():
    asyncio.create_task(start_rabbitmq_listener())
    await start_bot()

if __name__ == "__main__":
    asyncio.run(main())
