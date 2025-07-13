from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from core.config import BOT_TOKEN
from core.handlers import router

default_props = DefaultBotProperties(parse_mode="HTML")

bot = Bot(token=BOT_TOKEN, default=default_props)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)


async def send_message(chat_id: int, text: str):
    await bot.send_message(chat_id=chat_id, text=text)
