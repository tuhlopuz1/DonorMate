from datetime import datetime

from aiogram.fsm.state import State, StatesGroup


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
    ME_FILE = State()
    ME_START_DATE = State()
    ME_END_DATE = State()
    ME_PHONE_NUM = State()
    ME_COMMENT = State()
    DONOR_EARLIER = State()
    FEEDBACK = State()
    CONFIRM = State()


class MedicalExemptionUpdStates(StatesGroup):
    ME_FILE = State()
    ME_START_DATE = State()
    ME_END_DATE = State()
    ME_PHONE_NUM = State()
    ME_COMMENT = State()
    CONFIRM = State()


FIELD_NAMES_RU = {
    "fullname": "Имя",
    "surname": "Фамилия",
    "patronymic": "Отчество",
    "birth_date": "Дата рождения",
    "gender": "Пол",
    "university": "Университет",
    "group": "Группа",
    "weight": "Вес (кг)",
    "chronic_disease": "Хронические заболевания",
    "medical_exemption": "Медицинский отвод",
    "donor_earlier": "Ранее сдавал(а) кровь",
    "me_start_date": "Дата начала действия медицинского отвода",
    "me_end_date": "Дата окончания действия медицинского отвода",
    "me_phone_num": "Номер телефона врача",
    "me_comment": "Комментарий к медицинскому отводу",
    "feedback": "Контакт",
}


def format_value(value):
    if isinstance(value, bool):
        return "Да" if value else "Нет"
    if value in ["MALE", "FEMALE", "UNDEFINED"]:
        return {"MALE": "Мужской", "FEMALE": "Женский", "UNDEFINED": "Не указан"}.get(value, value)
    if value in ["YES", "NO", "ONCE"]:
        return {"YES": "Да", "NO": "Нет", "ONCE": "Один раз"}.get(value, value)
    if isinstance(value, str) and "T" in value and ":" in value:
        try:
            return datetime.fromisoformat(value).strftime("%d.%m.%Y")
        except ValueError:
            return value
    return value
