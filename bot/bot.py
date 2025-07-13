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


async def main():
    await bot.set_my_commands([BotCommand(command="start", description="Запустить мини-приложение")])
    await dp.start_polling(bot)
    logger.info("Bot polling")
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    queue = await channel.declare_queue("telegram_queue", durable=True)
    await queue.consume(on_message)
    print(" [*] Listening for messages...")
    await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
