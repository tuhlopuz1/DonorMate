import asyncio
import logging
from bot.core.dispatcher import dp, bot
from aiogram.types import BotCommand

logger = logging.getLogger(__name__)


async def main():
    await bot.set_my_commands([BotCommand(command="start", description="Запустить мини-приложение")])
    await dp.start_polling(bot)
    logger.info("Bot polling")

if __name__ == "__main__":
    asyncio.run(main)
