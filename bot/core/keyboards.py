from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
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
