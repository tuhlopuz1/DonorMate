from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Gender(Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    UNDEFINED = "UNDEFINED"


class DonorEarlier(Enum):
    NO = "NO"
    ONCE = "ONCE"
    YES = "YES"


class PostRegisterPayload(BaseModel):
    fullname: str
    surname: str
    patronymic: Optional[str] = None
    birth_date: str
    gender: Gender
    university: Optional[str] = None
    group: Optional[str] = None
    weight: int
    chronic_disease: bool
    medical_exemption: bool
    donor_earlier: DonorEarlier
    feedback: Optional[str] = None

    class Config:
        use_enum_values = True
