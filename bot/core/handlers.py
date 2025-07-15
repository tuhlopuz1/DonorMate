import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from aiogram.utils.markdown import hlink
from aiogram_calendar import DialogCalendarCallback
from aiohttp import ClientSession
from core.config import BACKEND_URL
from core.keyboards import (
    donor_earlier_kbd,
    empty_kbd,
    gender_kbd,
    inline_miniapp_kbd,
    menu_kbd,
    menu_register_kbd,
    yes_no_kbd,
)
from core.schemas import PostRegisterPayload
from core.states import (
    FIELD_NAMES_RU,
    MedicalExemptionUpdStates,
    RegisterStates,
    format_value,
)
from dependencies.api_dependencies import forward_exemption_to_fastapi, get_access_token
from dependencies.dialogcalendar import DialogCalendarNoCancel

router = Router()

logger = logging.getLogger(__name__)


@router.message(Command("start"))
async def handle_start(message: Message):
    async with ClientSession() as session:
        payload = {
            "user_id": message.from_user.id,
            "username": message.from_user.username,
            "tg_name": message.from_user.first_name,
        }
        await session.post(url=f"{BACKEND_URL}/telegram-register", json=payload)
    await message.answer("Выберите действие:", reply_markup=inline_miniapp_kbd)


@router.message(Command("menu"))
async def open_menu_command(message: Message):
    async with ClientSession() as session:
        response = await session.get(f"{BACKEND_URL}/is-registred/{message.chat.id}")
        if response.status == 200:
            await message.answer("Выберите пункт меню:", reply_markup=menu_kbd)
        elif response.status == 204:
            await message.answer("Для того чтобы перейти в меню - пройдите регистрацию", reply_markup=menu_register_kbd)
        elif response.status == 404:
            async with ClientSession() as session:
                payload = {
                    "user_id": message.from_user.id,
                    "username": message.from_user.username,
                    "tg_name": message.from_user.first_name,
                }
                await session.post(url=f"{BACKEND_URL}/telegram-register", json=payload)
            await message.answer("Для того чтобы перейти в меню - пройдите регистрацию", reply_markup=menu_register_kbd)


@router.callback_query(F.data == "menu")
async def open_menu(callback: CallbackQuery):
    await callback.answer()
    async with ClientSession() as session:
        response = await session.get(f"{BACKEND_URL}/is-registred/{callback.message.chat.id}")
        if response.status == 200:
            await callback.message.answer("Выберите пункт меню:", reply_markup=menu_kbd)
        elif response.status == 204:
            await callback.message.answer(
                "Для того чтобы перейти в меню - пройдите регистрацию", reply_markup=menu_register_kbd
            )
        elif response.status == 404:
            async with ClientSession() as session:
                payload = {
                    "user_id": callback.message.from_user.id,
                    "username": callback.message.from_user.username,
                    "tg_name": callback.message.from_user.first_name,
                }
                await session.post(url=f"{BACKEND_URL}/telegram-register", json=payload)
            await callback.message.answer(
                "Для того чтобы перейти в меню - пройдите регистрацию", reply_markup=menu_register_kbd
            )


@router.callback_query(F.data == "register")
async def start_registration(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.answer("Введите вашу фамилию:")
    await state.set_state(RegisterStates.SURNAME)


@router.message(RegisterStates.SURNAME)
async def input_surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await message.answer("Введите ваше имя:")
    await state.set_state(RegisterStates.FULLNAME)


@router.message(RegisterStates.FULLNAME)
async def input_fullname(message: Message, state: FSMContext):
    await state.update_data(fullname=message.text)
    await message.answer('Введите ваше отчество (если есть, иначе выберите "-"):', reply_markup=empty_kbd)
    await state.set_state(RegisterStates.PATRONYMIC)


@router.message(RegisterStates.PATRONYMIC)
async def input_patronymic(message: Message, state: FSMContext):
    patronymic = message.text
    await state.update_data(patronymic=None if patronymic == "-" else patronymic)
    calendar = DialogCalendarNoCancel()
    markup = await calendar.start_calendar()
    await message.answer("Выберите дату рождения:", reply_markup=markup)
    await state.set_state(RegisterStates.BIRTH_DATE)


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
    await message.answer('Введите ваш университет: (нажмите "-" для пропуска)', reply_markup=empty_kbd)
    await state.set_state(RegisterStates.UNIVERSITY)


@router.message(RegisterStates.UNIVERSITY)
async def input_university(message: Message, state: FSMContext):
    university = message.text
    await state.update_data(university=None if university == "-" else university)
    await message.answer('Введите вашу учебную группу: (нажмите "-" для пропуска)', reply_markup=empty_kbd)
    await state.set_state(RegisterStates.GROUP)


@router.message(RegisterStates.GROUP)
async def input_group(message: Message, state: FSMContext):
    group = message.text
    await state.update_data(group=None if group == "-" else group)
    await message.answer("Введите ваш вес (в кг):", reply_markup=ReplyKeyboardRemove())
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
    await message.answer("Есть ли у вас хронические заболевания?", reply_markup=yes_no_kbd)
    await state.set_state(RegisterStates.CHRONIC_DISEASE)


@router.message(RegisterStates.CHRONIC_DISEASE)
async def input_chronic_disease(message: Message, state: FSMContext):
    if message.text.lower() not in ("да", "нет"):
        await message.answer("Пожалуйста нажмите да или нет")
        return
    has_disease = message.text.lower() == "да"
    await state.update_data(chronic_disease=has_disease)
    await message.answer("Есть ли у вас медицинский отвод от донорства?", reply_markup=yes_no_kbd)
    await state.set_state(RegisterStates.MEDICAL_EXEMPTION)


@router.message(RegisterStates.MEDICAL_EXEMPTION)
async def input_medical_exemption(message: Message, state: FSMContext):
    if message.text.lower() == "да":
        await state.update_data(medical_exemption=True)
        calendar = DialogCalendarNoCancel()
        markup = await calendar.start_calendar()
        await message.answer("Выберите дату начала медицинского отвода:", reply_markup=markup)
        await state.set_state(RegisterStates.ME_START_DATE)
    elif message.text.lower() == "нет":
        await state.update_data(medical_exemption=False)
        await message.answer("Вы сдавали кровь раньше?", reply_markup=donor_earlier_kbd)
        await state.set_state(RegisterStates.DONOR_EARLIER)
    else:
        await message.answer("Пожалуйста нажмите да или нет")


@router.message(RegisterStates.ME_START_DATE)
async def wait_me_start_date(message: Message):
    await message.answer("Пожалуйста, выберите дату из календаря.")


@router.message(RegisterStates.ME_END_DATE)
async def wait_me_end_date(message: Message):
    await message.answer("Пожалуйста, выберите дату из календаря.")


@router.message(RegisterStates.ME_PHONE_NUM)
async def input_me_phone_num(message: Message, state: FSMContext):
    phone = message.text.strip()
    phone = None if phone == "-" else phone
    await state.update_data(me_phone_num=phone)
    await message.answer('Введите комментарий (нажмите "-" для пропуска):', reply_markup=empty_kbd)
    await state.set_state(RegisterStates.ME_COMMENT)


@router.message(RegisterStates.ME_COMMENT)
async def input_me_comment(message: Message, state: FSMContext):
    comment = message.text.strip()
    comment = None if comment == "-" else comment
    await state.update_data(me_comment=comment)
    await message.answer(
        "Пожалуйста, отправьте файл медицинского отвода (справку).", reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(RegisterStates.ME_FILE)


@router.message(RegisterStates.ME_FILE, F.content_type == "document")
async def handle_medical_exemption_file(message: Message, state: FSMContext):
    data = await state.get_data()
    token = await get_access_token(message.chat.id, message.chat.username)
    result = await forward_exemption_to_fastapi(
        token=token,
        start_date=data.get("me_start_date"),
        end_date=data.get("me_end_date"),
        file_id=message.document.file_id,
        file_name=message.document.file_name,
        mime_type=message.document.mime_type,
        medic_phone_num=data.get("me_phone_num"),
        comment=data.get("me_comment"),
    )
    if result.get("id") and result.get("url"):
        await state.update_data(medical_exemption_url=result["url"])
        await message.answer("Медицинский отвод успешно загружен.")
    else:
        await message.answer(f"Ошибка при загрузке: {result}")
    await message.answer("Вы сдавали кровь раньше?", reply_markup=donor_earlier_kbd)
    await state.set_state(RegisterStates.DONOR_EARLIER)


@router.message(RegisterStates.ME_FILE)
async def ask_correct_file(message: Message):
    await message.answer("Пожалуйста, отправьте файл в виде документа.")


@router.message(RegisterStates.DONOR_EARLIER)
async def input_donor_earlier(message: Message, state: FSMContext):
    text = message.text.lower()
    if text == "да":
        donor = "YES"
    elif text == "нет":
        donor = "NO"
    elif text == "однажды":
        donor = "ONCE"
    else:
        await message.answer("Пожалуйста выберите корректный вариант")
        return
    await state.update_data(donor_earlier=donor)
    await message.answer(
        text='Введите телефонный номер или email по которому с вами можно связаться (нажмите "-" для пропуска)',
        reply_markup=empty_kbd,
    )
    await state.set_state(RegisterStates.FEEDBACK)


@router.message(RegisterStates.FEEDBACK)
async def feedback_addr(message: Message, state: FSMContext):
    text = message.text.lower()
    feedback = None if text == "-" else text
    await state.update_data(feedback=feedback)
    data = await state.get_data()
    summary_lines = []
    for key, value in data.items():
        display_value = "Не указано" if value is None else format_value(value)
        if key == "medical_exemption_url" and value:
            summary_lines.append(f"Медицинский отвод: {hlink('ссылка', url=value)}")
        elif key != "medical_exemption_url":
            summary_lines.append(f"{FIELD_NAMES_RU.get(key, key)}: {display_value}")
    summary = "\n".join(summary_lines)
    await message.answer(
        f"Проверьте введённые данные:\n\n{summary}\n\nПодтвердите отправку?",
        reply_markup=yes_no_kbd,
        parse_mode="HTML",
    )
    await state.set_state(RegisterStates.CONFIRM)


@router.message(RegisterStates.CONFIRM)
async def confirm_registration(message: Message, state: FSMContext):
    if message.text.lower() == "да":
        data = await state.get_data()
        valid_data = PostRegisterPayload.model_validate(data)
        valid_data_dict = PostRegisterPayload.model_dump(valid_data)
        token = await get_access_token(message.chat.id, message.chat.username)
        async with ClientSession() as session:
            await session.post(
                f"{BACKEND_URL}/post-register", json=valid_data_dict, headers={"Authorization": f"Bearer {token}"}
            )
        await message.answer("Регистрация завершена. Спасибо!", reply_markup=ReplyKeyboardRemove())
        await message.answer("Выберите пункт меню: ", reply_markup=menu_kbd)
        await state.clear()
    else:
        await message.answer(
            "Регистрация отменена. Вы можете начать заново в меню",
            reply_markup=ReplyKeyboardRemove(),
        )
        await state.clear()


@router.callback_query(F.data == "medical_exemption_upd")
async def medical_exemption_upload(callback: CallbackQuery, state: FSMContext):
    calendar = DialogCalendarNoCancel()
    markup = await calendar.start_calendar()
    await callback.message.answer("Выберите дату начала медицинского отвода:", reply_markup=markup)
    await state.set_state(MedicalExemptionUpdStates.ME_START_DATE)


@router.message(MedicalExemptionUpdStates.ME_START_DATE)
async def me_start_date(message: Message):
    await message.answer("Пожалуйста, выберите дату из календаря.")


@router.message(MedicalExemptionUpdStates.ME_END_DATE)
async def me_end_date(message: Message):
    await message.answer("Пожалуйста, выберите дату из календаря.")


@router.message(MedicalExemptionUpdStates.ME_PHONE_NUM)
async def me_phone_num(message: Message, state: FSMContext):
    phone = message.text.strip()
    phone = None if phone == "-" else phone
    await state.update_data(me_phone_num=phone)
    await message.answer('Введите комментарий (нажмите "-" для пропуска):', reply_markup=empty_kbd)
    await state.set_state(MedicalExemptionUpdStates.ME_COMMENT)


@router.message(MedicalExemptionUpdStates.ME_COMMENT)
async def me_comment(message: Message, state: FSMContext):
    comment = message.text.strip()
    comment = None if comment == "-" else comment
    await state.update_data(me_comment=comment)
    await message.answer(
        "Пожалуйста, отправьте файл медицинского отвода (справку).", reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(MedicalExemptionUpdStates.ME_FILE)


@router.message(MedicalExemptionUpdStates.ME_FILE, F.content_type == "document")
async def medical_exemption_file(message: Message, state: FSMContext):
    data = await state.get_data()
    summary_lines = []
    for key, value in data.items():
        display_value = "Не указано" if value is None else format_value(value)
        summary_lines.append(f"{FIELD_NAMES_RU.get(key, key)}: {display_value}")
    summary = "\n".join(summary_lines)
    await message.answer(
        f"Проверьте введённые данные:\n\n{summary}\n\nПодтвердите отправку?",
        reply_markup=yes_no_kbd,
        parse_mode="HTML",
    )
    await state.update_data(
        me_file_id=message.document.file_id,
        me_file_name=message.document.file_name,
        me_mime_type=message.document.mime_type,
    )
    await state.set_state(MedicalExemptionUpdStates.CONFIRM)


@router.message(MedicalExemptionUpdStates.ME_FILE)
async def correct_file(message: Message):
    await message.answer("Пожалуйста, отправьте файл в виде документа.")


@router.message(MedicalExemptionUpdStates.CONFIRM)
async def confirm_me(message: Message, state: FSMContext):
    if message.text.lower() == "да":
        data = await state.get_data()
        token = await get_access_token(message.chat.id, message.chat.username)

        if not data.get("me_file_id"):
            await message.answer("Файл не найден, загрузите медицинский отвод заново.")
            await state.clear()
            return

        result = await forward_exemption_to_fastapi(
            token=token,
            start_date=data.get("me_start_date"),
            end_date=data.get("me_end_date"),
            file_id=data["me_file_id"],
            file_name=data["me_file_name"],
            mime_type=data.get("me_mime_type"),
            medic_phone_num=data.get("me_phone_num"),
            comment=data.get("me_comment"),
        )
        if result.get("id") and result.get("url"):
            await message.answer(
                f"Медицинский отвод успешно загружен. {hlink('ссылка', url=result['url'])}",
                reply_markup=ReplyKeyboardRemove(),
                parse_mode="HTML",
            )
        else:
            await message.answer(f"Ошибка при загрузке: {result}")
        await state.clear()
    else:
        await message.answer(
            "Отправка отменена. Вы можете начать заново в меню",
            reply_markup=ReplyKeyboardRemove(),
        )
        await state.clear()


@router.callback_query(DialogCalendarCallback.filter())
async def process_calendar_selection(
    callback_query: CallbackQuery, callback_data: DialogCalendarCallback, state: FSMContext
):
    calendar = DialogCalendarNoCancel()
    selected, selected_date = await calendar.process_selection(callback_query, callback_data)

    if selected:
        iso_date = selected_date.isoformat()
        current_state = await state.get_state()

        if current_state == RegisterStates.BIRTH_DATE:
            await state.update_data(birth_date=iso_date)
            await callback_query.message.answer("Ваш пол?", reply_markup=gender_kbd)
            await state.set_state(RegisterStates.GENDER)

        elif current_state == RegisterStates.ME_START_DATE:
            await state.update_data(me_start_date=iso_date)
            calendar_markup = await calendar.start_calendar()
            await callback_query.message.answer(
                "Выберите дату окончания медицинского отвода:", reply_markup=calendar_markup
            )
            await state.set_state(RegisterStates.ME_END_DATE)

        elif current_state == RegisterStates.ME_END_DATE:
            await state.update_data(me_end_date=iso_date)
            await callback_query.message.answer(
                "Введите номер телефона врача (нажмите '-' для пропуска):", reply_markup=empty_kbd
            )
            await state.set_state(RegisterStates.ME_PHONE_NUM)

        elif current_state == MedicalExemptionUpdStates.ME_START_DATE:
            await state.update_data(me_start_date=iso_date)
            calendar_markup = await calendar.start_calendar()
            await callback_query.message.answer(
                "Выберите дату окончания медицинского отвода:", reply_markup=calendar_markup
            )
            await state.set_state(MedicalExemptionUpdStates.ME_END_DATE)

        elif current_state == MedicalExemptionUpdStates.ME_END_DATE:
            await state.update_data(me_end_date=iso_date)
            await callback_query.message.answer(
                "Введите номер телефона врача (нажмите '-' для пропуска):", reply_markup=empty_kbd
            )
            await state.set_state(MedicalExemptionUpdStates.ME_PHONE_NUM)

    elif selected_date:
        await callback_query.message.edit_reply_markup(reply_markup=selected_date)
    else:
        await callback_query.answer()
