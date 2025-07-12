import asyncio
import logging
from core.dispatcher import dp, bot

logger = logging.getLogger(__name__)


async def main():
    await dp.start_polling(bot)
    logger.info("Bot polling")

if __name__ == "__main__":
    asyncio.run(main)
