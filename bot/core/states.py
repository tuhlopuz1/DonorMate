from datetime import datetime
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiohttp.client import ClientSession
from core.handlers import router
from core.keyboards import gender_keyboard, yes_no_keyboard
from core.config import BACKEND_URL


class RegisterStates(StatesGroup):
    FULLNAME = State()
    SURNAME = State()
    PATRONYMIC = State()
    BIRTH_DATE = State()
    GENDER = State()
    UNIVERSITY = State()
    GROUP = State()
    WEIGHT = State()
    CHRONIC_DISEASE = State()
    MEDICAL_EXEMPTION = State()
    DONOR_EARLIER = State()
    CONFIRM = State()


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

    await state.update_data(birth_date=birth_date)
    await message.answer("Ваш пол?", reply_markup=gender_keyboard)
    await state.set_state(RegisterStates.GENDER)


@router.message(RegisterStates.GENDER)
async def input_gender(message: Message, state: FSMContext):
    text = message.text.lower()
    if "Мужской" in text:
        gender = "MALE"
    elif "Женский" in text:
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
    await message.answer("Вы сдавали кровь раньше? (да/нет)")
    await state.set_state(RegisterStates.DONOR_EARLIER)


@router.message(RegisterStates.DONOR_EARLIER)
async def input_donor_earlier(message: Message, state: FSMContext):
    text = message.text.lower()
    if text == "Да, был(а)":
        donor = "YES"
    elif text == "Не был(а)":
        donor = "NO"
    else:
        donor = "ONCE"

    await state.update_data(donor_earlier=donor)

    data = await state.get_data()
    summary = "\n".join(f"{key}: {value}" for key, value in data.items())

    await message.answer(
        f"Проверьте введённые данные:\n\n{summary}\n\nПодтвердите отправку?",
        reply_markup=yes_no_keyboard
    )
    await state.set_state(RegisterStates.CONFIRM)


@router.message(RegisterStates.CONFIRM)
async def confirm_registration(message: Message, state: FSMContext):
    if message.text.lower() == "да":
        data = await state.get_data()
        async with ClientSession() as session:
            await session.post(f"{BACKEND_URL}/post-register", json=data)

        await message.answer("Регистрация завершена. Спасибо!")
        await state.clear()
    else:
        await message.answer("Регистрация отменена. Вы можете начать заново, нажав /menu и выбрав регистрацию")
        await state.clear()
