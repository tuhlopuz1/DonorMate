from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from core.config import FRONTEND_URL

miniapp_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="Открыть MiniApp",
                web_app=WebAppInfo(url=FRONTEND_URL)
            )
        ]
    ],
    resize_keyboard=True,
)

inline_miniapp_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Открыть мини-приложение",
                web_app=WebAppInfo(url=FRONTEND_URL)
            )
        ]
    ]
)