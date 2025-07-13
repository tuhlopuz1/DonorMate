from aiogram.types import WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from core.config import FRONTEND_URL


inline_miniapp_keyboard = InlineKeyboardMarkup(
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

menu_register_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Вписать медицинские данные",
                callback_data="register",
            )
        ],
    ]
)

gender_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Мужской"), KeyboardButton(text="Женский")],
        [KeyboardButton(text="Не указывать")],
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

yes_no_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Да"), KeyboardButton(text="Нет")]
    ]
)

donor_earlier_kboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Да, был(а)")],
        [KeyboardButton(text="Был(а) однажды")],
        [KeyboardButton(text="Нет, не был(а)")]
    ]
)
