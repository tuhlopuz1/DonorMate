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
    DONOR_EARLIER = State()
    CONFIRM = State()
