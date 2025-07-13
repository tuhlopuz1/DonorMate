from datetime import datetime
from pydantic import BaseModel
from typing import Optional
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


class ProfileResponse(BaseModel):
    user_id: int
    username: Optional[str] = None
    tg_name: Optional[str] = None
    role: Role
    created_at: datetime
    fullname: Optional[str] = None
    surname: Optional[str] = None
    patronymic: Optional[str] = None
    birth_date: Optional[datetime] = None
    gender: Optional[Gender] = Gender.UNDEFINED
    university: Optional[str] = None
    group: Optional[str] = None
    weight: Optional[int] = None
    chronic_disease: Optional[bool] = None
    medical_exemption: Optional[bool] = None
    donor_earlier: Optional[DonorEarlier] = None

    model_config = {"from_attributes": True}
