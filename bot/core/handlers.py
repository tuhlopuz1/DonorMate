from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiohttp import ClientSession
from core.config import BACKEND_URL
from core.keyboards import inline_miniapp_keyboard, menu_register_keyboard

router = Router()


class RegisterStates(StatesGroup):
    USER_NAME_SURNAME_PATRONYMIC = State()


@router.message(Command("start"))
async def handle_start(message: Message):
    async with ClientSession() as session:
        payload = {
            "user_id": message.from_user.id,
            "username": message.from_user.username,
            "tg_name": message.from_user.first_name
        }
        await session.post(url=f"{BACKEND_URL}/telegram-register", json=payload)

    await message.answer("Выберите действие:", reply_markup=inline_miniapp_keyboard)


@router.message()
async def echo(message: Message):
    await message.reply("Используйте /start чтобы открыть МиниПриложение или меню")


@router.callback_query(F.data == "menu")
async def open_menu(callback: CallbackQuery):
    await callback.answer()
    async with ClientSession() as session:
        response = await session.get(f"{BACKEND_URL}/is-registred/{callback.message.chat.id}")
        if response.status == 200:
            pass
        elif response.status == 204:
            await callback.message.answer("Выберите пункт меню:", reply_markup=menu_register_keyboard)


@router.callback_query(F.data == "register")
async def start_post_registration(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer(text="Введите свои имя фамилию и отчество")
    await state.set_state(RegisterStates.USER_NAME_SURNAME_PATRONYMIC)


@router.message(RegisterStates.USER_NAME_SURNAME_PATRONYMIC)
async def user_nsp(message: Message, state: FSMContext):
    await message.answer(f"Ваше ФИО: {message.text}")
    await state.clear()
