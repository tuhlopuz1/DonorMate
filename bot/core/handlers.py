import logging
from datetime import datetime

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiohttp import ClientSession
from core.config import BACKEND_URL
from core.keyboards import (
    donor_earlier_kboard,
    gender_keyboard,
    inline_miniapp_keyboard,
    menu_register_keyboard,
    yes_no_keyboard,
)
from core.states import FIELD_NAMES_RU, RegisterStates, format_value
from dependencies.initdata import create_init_data

router = Router()


@router.message(Command("start"))
async def handle_start(message: Message):
    async with ClientSession() as session:
        payload = {
            "user_id": message.from_user.id,
            "username": message.from_user.username,
            "tg_name": message.from_user.first_name,
        }
        await session.post(url=f"{BACKEND_URL}/telegram-register", json=payload)

    await message.answer("Выберите действие:", reply_markup=inline_miniapp_keyboard)


@router.message(Command("menu"))
async def open_menu_command(message: Message):
    async with ClientSession() as session:
        response = await session.get(f"{BACKEND_URL}/is-registred/{message.chat.id}")
        if response.status == 200:
            pass
        elif response.status == 204:
            await message.answer("Выберите пункт меню:", reply_markup=menu_register_keyboard)


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
async def start_registration(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Введите ваше имя:")
    await state.set_state(RegisterStates.FULLNAME)


@router.message(RegisterStates.FULLNAME)
async def input_fullname(message: Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    await message.answer("Введите вашу фамилию:")
    await state.set_state(RegisterStates.SURNAME)


@router.message(RegisterStates.SURNAME)
async def input_surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await message.answer("Введите ваше отчество (если есть, иначе напишите -):")
    await state.set_state(RegisterStates.PATRONYMIC)


@router.message(RegisterStates.PATRONYMIC)
async def input_patronymic(message: Message, state: FSMContext):
    patronymic = message.text
    await state.update_data(patronymic=None if patronymic == "-" else patronymic)
    await message.answer("Введите дату рождения (ДД.ММ.ГГГГ):")
    await state.set_state(RegisterStates.BIRTH_DATE)


@router.message(RegisterStates.BIRTH_DATE)
async def input_birthdate(message: Message, state: FSMContext):
    try:
        birth_date = datetime.strptime(message.text, "%d.%m.%Y")
    except ValueError:
        await message.answer("Неверный формат. Введите дату в формате ДД.ММ.ГГГГ:")
        return

    await state.update_data(birth_date=str(birth_date.isoformat()))
    await message.answer("Ваш пол?", reply_markup=gender_keyboard)
    await state.set_state(RegisterStates.GENDER)


@router.message(RegisterStates.GENDER)
async def input_gender(message: Message, state: FSMContext):
    text = message.text.lower()
    if "мужской" in text:
        gender = "MALE"
    elif "женский" in text:
        gender = "FEMALE"
    else:
        gender = "UNDEFINED"

    await state.update_data(gender=gender)
    await message.answer("Введите ваш университет:")
    await state.set_state(RegisterStates.UNIVERSITY)


@router.message(RegisterStates.UNIVERSITY)
async def input_university(message: Message, state: FSMContext):
    await state.update_data(university=message.text)
    await message.answer("Введите вашу учебную группу:")
    await state.set_state(RegisterStates.GROUP)


@router.message(RegisterStates.GROUP)
async def input_group(message: Message, state: FSMContext):
    await state.update_data(group=message.text)
    await message.answer("Введите ваш вес (в кг):")
    await state.set_state(RegisterStates.WEIGHT)


@router.message(RegisterStates.WEIGHT)
async def input_weight(message: Message, state: FSMContext):
    try:
        weight = int(message.text)
        if weight < 30 or weight > 300:
            raise ValueError
    except ValueError:
        await message.answer("Пожалуйста, введите корректный вес в кг (число от 30 до 300):")
        return

    await state.update_data(weight=weight)
    await message.answer("Есть ли у вас хронические заболевания?", reply_markup=yes_no_keyboard)
    await state.set_state(RegisterStates.CHRONIC_DISEASE)


@router.message(RegisterStates.CHRONIC_DISEASE)
async def input_chronic_disease(message: Message, state: FSMContext):
    has_disease = message.text.lower() == "да"
    await state.update_data(chronic_disease=has_disease)
    await message.answer("Есть ли у вас медицинский отвод от донорства?", reply_markup=yes_no_keyboard)
    await state.set_state(RegisterStates.MEDICAL_EXEMPTION)


@router.message(RegisterStates.MEDICAL_EXEMPTION)
async def input_medical_exemption(message: Message, state: FSMContext):
    exempted = message.text.lower() == "да"
    await state.update_data(medical_exemption=exempted)
    await message.answer("Вы сдавали кровь раньше?", reply_markup=donor_earlier_kboard)
    await state.set_state(RegisterStates.DONOR_EARLIER)


@router.message(RegisterStates.DONOR_EARLIER)
async def input_donor_earlier(message: Message, state: FSMContext):
    text = message.text.lower()
    if text == "да":
        donor = "YES"
    elif text == "нет":
        donor = "NO"
    else:
        donor = "ONCE"

    await state.update_data(donor_earlier=donor)

    data = await state.get_data()
    summary = "\n".join(f"{FIELD_NAMES_RU.get(key, key)}: {format_value(value)}" for key, value in data.items())
    await message.answer(
        f"Проверьте введённые данные:\n\n{summary}\n\nПодтвердите отправку?", reply_markup=yes_no_keyboard
    )
    await state.set_state(RegisterStates.CONFIRM)


@router.message(RegisterStates.CONFIRM)
async def confirm_registration(message: Message, state: FSMContext):
    if message.text.lower() == "да":
        data = await state.get_data()
        init_data = create_init_data(message.chat.id, message.chat.username)
        async with ClientSession() as session:
            response = await session.post(f"{BACKEND_URL}/get-token", json={"InitData": str(init_data)})
            tokens = await response.json()

            await session.post(
                f"{BACKEND_URL}/post-register", json=data, headers={"Authorization": f"Bearer {tokens['access']}"}
            )
            logging.info(tokens)
        await message.answer("Регистрация завершена. Спасибо!", reply_markup=ReplyKeyboardRemove())
        await state.clear()
    else:
        await message.answer(
            "Регистрация отменена. Вы можете начать заново, нажав /menu и выбрав регистрацию",
            reply_markup=ReplyKeyboardRemove(),
        )
        await state.clear()
