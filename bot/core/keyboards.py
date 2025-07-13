from aiogram.types import WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from core.config import FRONTEND_URL


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
