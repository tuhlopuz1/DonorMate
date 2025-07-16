import os

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import FSInputFile
from core.config import BOT_TOKEN
from core.handlers import router
from dependencies.qr_code_gen import generate_temp_qr

default_props = DefaultBotProperties(parse_mode="HTML")

bot = Bot(token=BOT_TOKEN, default=default_props)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)


async def send_message(chat_id: int, text: str):
    await bot.send_message(chat_id=chat_id, text=text)


async def send_qr(chat_id: int, text: str, data: str):
    qr_tmp = generate_temp_qr(data)
    qr = FSInputFile(qr_tmp)
    await bot.send_photo(chat_id, photo=qr, caption=text)
    os.remove(qr_tmp)
