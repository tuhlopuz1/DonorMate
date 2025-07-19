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
    FMBA = "ЦК ФМБА"
    GAUR = "ЦК им. Гаврилова"


class UserClass(Enum):
    EXT = "Внешний донор"
    STU = "Студент МИФИ"
    STF = "Сотрудник МИФИ"


class NotificationEnum(Enum):
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class InitDataPayload(BaseModel):
    InitData: str


class TokensResponse(BaseModel):
    access: str
    refresh: str
    role: Role


class RefreshResponse(BaseModel):
    new_access_token: str


class PostRegisterPayload(BaseModel):
    fsp: str
    group: Optional[str] = None
    user_class: UserClass
    social: Optional[str] = None


class ProfileResponse(BaseModel):
    id: int
    phone: int
    fsp: str
    group: Optional[str] = None
    user_class: UserClass
    social: Optional[str] = None
    donations_fmba: int
    donations_gaur: int
    donations: Optional[int] = None
    last_don_gaur: Optional[datetime] = None
    last_don_fmba: Optional[datetime] = None

    model_config = {"from_attributes": True}


class EventPayload(BaseModel):
    name: Optional[str] = None
    start_date: datetime
    end_date: datetime
    description: str
    place: Place


class EventResponse(BaseModel):
    id: UUID
    name: str
    description: str
    place: Place
    registred: int
    start_date: datetime
    end_date: datetime
    created_at: datetime


class EventSchema(BaseModel):
    id: UUID
    name: str
    description: str
    place: Place
    registred: int
    start_date: datetime
    end_date: datetime
    created_at: datetime
    is_registred: bool = False

    model_config = {"from_attributes": True}


class MedicalExemptionResponse(BaseModel):
    id: UUID
    url: str


class UpdateInfoPayload(BaseModel):
    phone: Optional[int] = None
    fsp: Optional[str] = None
    group: Optional[str] = None
    user_class: Optional[UserClass] = None
    social: Optional[str] = None
    donations_fmba: Optional[int] = None
    donations_gaur: Optional[int] = None
    donations: Optional[int] = None
    last_don_gaur: Optional[datetime] = None
    last_don_fmba: Optional[datetime] = None


class MetricsResponse(BaseModel):
    users_count: int
    donations_count: int
    donations_fmba_count: int
    donations_gaur_count: int
    new_events_count: int
    ended_events_count: int


class RoleMetricsResponse(BaseModel):
    users_count: int
    admins_count: int
    donors_count_fmba: int
    const_donors_count_fmba: int
    donors_count_gaur: int
    const_donors_count_gaur: int


class QuestionPayload(BaseModel):
    question: Optional[str] = None


class MesagePayload(BaseModel):
    message: str
