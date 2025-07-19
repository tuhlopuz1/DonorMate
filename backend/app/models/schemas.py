# from datetime import date, datetime
from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class Role(Enum):
    DONOR = "DONOR"
    ADMIN = "ADMIN"


class Place(Enum):
    FMBA = "г. Москва, ул. Щукинская д. 6, корп. 2"
    GAUR = "г. Москва, ул. Поликарпова, д. 14, корп. 2"


class UserClass(Enum):
    EXT = "Внешний донор"
    STU = "Студент МИФИ"
    STF = "Сотрудник МИФИ"


class InitDataPayload(BaseModel):
    InitData: str


class TokensResponse(BaseModel):
    access: str
    refresh: str


class RefreshResponse(BaseModel):
    new_access_token: str


class PostRegisterPayload(BaseModel):
    fsp: str
    group: Optional[str] = None
    user_class: UserClass


class ProfileResponse(BaseModel):
    id: int
    phone: str
    fsp: str
    group: str
    user_class: UserClass
    donations: int

    model_config = {"from_attributes": True}


class EventPayload(BaseModel):
    name: Optional[str] = None
    max_donors: int
    start_date: datetime
    end_date: datetime
    organizer: int
    description: str
    place: str


class EventResponse(BaseModel):
    id: UUID
    name: str
    description: str
    organizer: int
    max_donors: int
    registred: int
    start_date: datetime
    end_date: datetime
    created_at: datetime


class MedicalExemptionResponse(BaseModel):
    id: UUID
    url: str


class UpdateInfoPayload(BaseModel):
    fullname: Optional[str] = None


class DonorResponse(BaseModel):
    id: int
    fullname: str
    surname: str
    patronymic: str
    username: str
    donations: int


class MetricsResponse(BaseModel):
    users_count: int
    donations_count: int
    new_events_count: int
    ended_events_count: int


class RoleMetricsResponse(BaseModel):
    users_count: int
    admins_count: int
    donors_count: int
    const_donors_count: int


class QAPayload(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None
