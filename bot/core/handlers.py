from aiogram import types, Router
from aiogram.filters import Command
from aiohttp import ClientSession
from core.config import BACKEND_URL
from core.keyboards import inline_miniapp_keyboard

router = Router()


@router.message(Command("start"))
async def handle_start(message: types.Message):
    async with ClientSession() as session:
        payload = {
            "user_id": message.from_user.id,
            "username": message.from_user.username,
            "tg_name": message.from_user.first_name
        }
        async with session.post(url=f"{BACKEND_URL}/register", json=payload) as resp:
            _ = await resp.json()

    await message.answer("To open miniapp click on the button below", reply_markup=inline_miniapp_keyboard)


@router.message()
async def echo(message: types.Message):
    await message.reply("Use /start to open miniapp")
