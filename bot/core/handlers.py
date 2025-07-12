from aiogram import types, Router
from aiogram.filters import Command
from core.keyboards import inline_miniapp_keyboard

router = Router()


@router.message(Command("start"))
async def handle_start(message: types.Message):
    await message.answer("To open miniapp click on the button below", reply_markup=inline_miniapp_keyboard, )


@router.message()
async def echo(message: types.Message):
    await message.reply("Напиши /start чтобы открыть мини-приложение")
