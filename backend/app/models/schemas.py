from datetime import datetime
from pydantic import BaseModel


class TelegramUserInfoPayload(BaseModel):
    id: int
    username: str
    tg_name: str


class InitDataPayload(BaseModel):
    InitData: str


class TokensResponse(BaseModel):
    access: str
    refresh: str


class PostRegisterPayload(BaseModel):
    fullname: str
    surname: str
    patronymic: str
    birth_date: datetime
