from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
    WebAppInfo,
)
from core.config import FRONTEND_URL

inline_miniapp_kbd = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Открыть мини-приложение",
                web_app=WebAppInfo(url=FRONTEND_URL),
            )
        ],
        [
            InlineKeyboardButton(
                text="Открыть меню",
                callback_data="menu",
            )
        ],
    ]
)

menu_register_kbd = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Вписать медицинские данные",
                callback_data="register",
            )
        ],
    ]
)

menu_kbd = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Список мероприятий",
                callback_data="list",
            )
        ],
    ]
)


gender_kbd = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Мужской"), KeyboardButton(text="Женский")],
        [KeyboardButton(text="Не указывать")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True,
)

yes_no_kbd = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Да"), KeyboardButton(text="Нет")]])

donor_earlier_kbd = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Да")], [KeyboardButton(text="Нет")], [KeyboardButton(text="Однажды")]]
)
