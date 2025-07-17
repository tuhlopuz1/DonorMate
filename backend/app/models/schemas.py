from datetime import date, datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Role(Enum):
    DONOR = "DONOR"
    ADMIN = "ADMIN"


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


class RefreshResponse(BaseModel):
    new_access_token: str


class PostRegisterPayload(BaseModel):
    fullname: str
    surname: str
    patronymic: Optional[str] = None
    birth_date: date
    gender: Gender
    university: Optional[str] = None
    group: Optional[str] = None
    weight: int
    chronic_disease: bool
    medical_exemption: bool
    donor_earlier: DonorEarlier
    feedback: Optional[str] = None


class ProfileResponse(BaseModel):
    user_id: int
    username: Optional[str] = None
    tg_name: Optional[str] = None
    role: Role
    created_at: datetime
    fullname: Optional[str] = None
    surname: Optional[str] = None
    patronymic: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[Gender] = Gender.UNDEFINED
    university: Optional[str] = None
    group: Optional[str] = None
    weight: Optional[int] = None
    chronic_disease: Optional[bool] = None
    medical_exemption: Optional[bool] = None
    donor_earlier: Optional[DonorEarlier] = None

    model_config = {"from_attributes": True}


class EventPayload(BaseModel):
    name: Optional[str] = None
    max_donors: int
    start_date: datetime
    end_date: datetime
    organizer: int
    description: str
    place: str


class MedicalExemptionResponse(BaseModel):
    id: UUID
    url: str


class UpdateInfoPayload(BaseModel):
    fullname: Optional[str] = None
    surname: Optional[str] = None
    patronymic: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[Gender] = None
    university: Optional[str] = None
    group: Optional[str] = None
    weight: Optional[int] = None
    chronic_disease: Optional[bool] = None
    medical_exemption: Optional[bool] = None
    donor_earlier: Optional[DonorEarlier] = None
    feedback: Optional[str] = None
