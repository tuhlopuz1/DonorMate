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
    ]
)

menu_kbd = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="foo")]])


register_miniapp_kbd = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Открыть МиниПриложение", web_app=WebAppInfo(url=f"{FRONTEND_URL}welcome"))]
    ]
)

phone_share_num = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Поделиться номером", request_contact=True)]],
    one_time_keyboard=True,
)

yes_no_kbd = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Да"), KeyboardButton(text="Нет")]], one_time_keyboard=True
)
