import logging
import re

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiohttp import ClientSession
from core.config import ADMIN_IDS, BACKEND_URL
from core.keyboards import (
    inline_miniapp_kbd,
    menu_kbd,
    phone_share_num,
    register_miniapp_kbd,
    yes_no_kbd,
)
from core.states import AdminState, TGRegister
from dependencies.api_dependencies import generate_secure_code, get_access_token
from models.redis_adapter import redis_adapter

router = Router()

logger = logging.getLogger(__name__)


@router.message(Command("start"))
async def handle_start(message: Message, state: FSMContext):
    async with ClientSession() as session:
        async with session.get(f"{BACKEND_URL}/is-registred/{message.chat.id}") as resp:
            if resp.status == 200:
                await message.answer("Выберите действие:", reply_markup=inline_miniapp_kbd)
            elif resp.status == 204:
                await message.answer(
                    text=(
                        "Для того чтобы начать пользоваться ботом, пожалуйста,"
                        "\n поделитесь номером телефона или введите его вручную."
                    ),
                    reply_markup=phone_share_num,
                )
                await state.set_state(TGRegister.PHONE_NUMBER)


@router.message(Command("menu"))
async def open_menu_command(message: Message, state: FSMContext):
    async with ClientSession() as session:
        response = await session.get(f"{BACKEND_URL}/is-registred/{message.chat.id}")
        if response.status == 200:
            await message.answer("Выберите пункт меню:", reply_markup=menu_kbd)
        elif response.status == 204:
            await message.answer(
                "Для того чтобы перейти в меню введите свой номер телефона\n(или поделитесь им)",
                reply_markup=phone_share_num,
            )
            await state.set_state(TGRegister.PHONE_NUMBER)


@router.callback_query(F.data == "menu")
async def open_menu(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    async with ClientSession() as session:
        response = await session.get(f"{BACKEND_URL}/is-registred/{callback.message.chat.id}")
        if response.status == 200:
            await callback.message.answer("Выберите пункт меню:", reply_markup=menu_kbd)
        elif response.status == 204:
            await callback.message.answer(
                "Для того чтобы перейти в меню введите свой номер телефона\n(или поделитесь им)",
                reply_markup=phone_share_num,
            )
            await state.set_state(TGRegister.PHONE_NUMBER)


@router.message(Command("code"))
async def get_or_check_admin_code(message: Message, state: FSMContext):
    if message.chat.id in ADMIN_IDS:
        code = generate_secure_code()
        await redis_adapter.set(f"admin_code:{code}", message.chat.id, expire=600)
        await message.answer(
            text=(
                "Чтобы назначить кого-то админом, попросите ввести команду:\n"
                "```/code```\n"
                f"Затем введите этот код:\n```{code}```\n"
                "_Код действителен в течение 10 минут_"
            ),
            parse_mode="Markdown",
        )
    else:
        async with ClientSession() as session:
            response = await session.get(f"{BACKEND_URL}/is-registred/{message.chat.id}")
            if response.status == 204:
                await session.post(url=f"{BACKEND_URL}/pre-reg-no-phone", params={"id": message.chat.id})
                await state.set_state(AdminState.ADMIN_CODE)
                await message.answer("Введите код отправленный вам админом")
            elif response.status == 200:
                await state.set_state(AdminState.ADMIN_CODE)
                await message.answer("Введите код отправленный вам админом")


@router.message(TGRegister.PHONE_NUMBER)
async def validate_phone_num(message: Message, state: FSMContext):
    phone_number = message.text
    phone_contact = message.contact.phone_number
    if phone_number:
        cleaned_number = re.sub(r"[^0-9]", "", phone_number.strip())
    elif phone_contact:
        cleaned_number = re.sub(r"[^0-9]", "", phone_contact.strip())
    else:
        await message.answer("Это не номер телефона.", reply_markup=phone_share_num)
        return
    if len(cleaned_number) == 11:
        cleaned_number = cleaned_number[1:]
    if len(cleaned_number) == 10:
        async with ClientSession() as session:
            async with session.get(f"{BACKEND_URL}/check-num/{cleaned_number}") as resp:
                if resp.status == 200:
                    name = resp.json()["message"]
                    await state.set_data(num=cleaned_number, id=message.chat.id)
                    await message.answer(f"Ваше имя - {name}?", reply_markup=yes_no_kbd)
                    await state.set_state(TGRegister.FSP_CONFIRM)
                elif resp.status == 204:
                    await session.post(
                        f"{BACKEND_URL}/pre-register", params={"num": cleaned_number, "id": message.chat.id}
                    )
                    await message.answer(
                        "Для продолжения перейдите в МиниПриложение", reply_markup=register_miniapp_kbd
                    )
                    await state.clear()
    else:
        await message.answer(
            "Неверный формат номера телефона. Пожалуйста, введите номер еще раз.", reply_markup=phone_share_num
        )
        return


@router.message(TGRegister.FSP_CONFIRM)
async def confirm_existing_fsp(message: Message, state: FSMContext):
    text = message.text.lower()
    if text == "да":
        data = await state.get_data()
        async with ClientSession() as session:
            await session.post(f"{BACKEND_URL}/link-number", params=data)
    elif text == "нет":
        data = await state.get_data()
        await session.post(f"{BACKEND_URL}/pre-register", params={"num": data["num"], "id": message.chat.id})
        await message.answer("Для продолжения перейдите в МиниПриложение", reply_markup=register_miniapp_kbd)
        await state.clear()
    else:
        await message.answer("Пожалуйста, выберите корректный вариант", reply_markup=yes_no_kbd)
        return


@router.message(AdminState.ADMIN_CODE)
async def validate_code(message: Message, state: FSMContext):
    code = message.text
    token = await get_access_token(message.chat.id, message.chat.username)
    async with ClientSession() as session:
        async with session.post(
            f"{BACKEND_URL}/set-organizer/{code}", headers={"Authorization": f"Bearer {token}"}
        ) as resp:
            if resp.status == 200:
                await message.answer("Теперь вы организатор мероприятий.")
                await state.clear()
            elif resp.status == 401:
                await message.answer("Ошибка авторизации. Попробуйте снова")
                return
            else:
                await message.answer("Код не верен. Попробуйте ещё раз или используйте другую команду")
                return
