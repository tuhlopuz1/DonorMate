from aiogram import types, Router
from aiogram.filters import Command

router = Router()


@router.message(Command("start"))
async def handle_start(message: types.Message):
    await message.answer("Started")
