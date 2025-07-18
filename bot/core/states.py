from aiogram.fsm.state import State, StatesGroup


class TGRegister(StatesGroup):
    PHONE_NUMBER = State()
    FSP_CONFIRM = State()


class AdminState(StatesGroup):
    ADMIN_CODE = State()
