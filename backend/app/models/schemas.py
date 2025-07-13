from datetime import datetime
from pydantic import BaseModel
from enum import Enum


class Role(Enum):
    DONOR = "DONOR"
    ADMON = "ADMIN"


class Gender(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    UNDEFINED = "UNDEFINED"


class DonorEarlier(Enum):
    NO = "NO"
    ONCE = "ONCE"
    YES = "YES"


class TelegramUserInfoPayload(BaseModel):
    user_id: int
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
    gender: Gender
    university: str
    group: str
    weight: int
    chronic_disease: bool
    medical_exemption: bool
    donor_earlier: DonorEarlier
