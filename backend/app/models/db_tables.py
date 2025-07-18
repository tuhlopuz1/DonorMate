from datetime import date, datetime
from typing import Optional
from uuid import UUID, uuid4

import inflect
from app.models.schemas import Role
from sqlalchemy import (
    BigInteger,
    Boolean,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    Uuid,
)
from sqlalchemy.orm import (
    Mapped,
    declarative_base,
    declared_attr,
    mapped_column,
    relationship,
)
from sqlalchemy.sql import func

p = inflect.engine()


class Base:
    @declared_attr
    def __tablename__(cls):
        return p.plural(cls.__name__.lower())


Base = declarative_base(cls=Base)


class User(Base):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    phone: Mapped[int] = mapped_column(BigInteger, nullable=False)
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.DONOR)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    notifications_bool: Mapped[bool] = mapped_column(Boolean, default=True)

    info: Mapped[Optional["Information"]] = relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan"
    )

    registrations_list: Mapped[list["Registration"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    events: Mapped[list["Event"]] = relationship(back_populates="organizer_user", cascade="all, delete-orphan")


class Information(Base):
    phone: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.phone", ondelete="CASCADE"), primary_key=True)
    fsp: Mapped[str] = mapped_column(String)
    group: Mapped[str] = mapped_column(String, nullable=True)
    donations: Mapped[int] = mapped_column(Integer, default=0)

    user: Mapped["User"] = relationship(back_populates="info")


class MedicalExemption(Base):
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=True)
    medic_phone_num: Mapped[str] = mapped_column(String, nullable=True)
    comment: Mapped[str] = mapped_column(String, nullable=True)
    url: Mapped[str] = mapped_column(String, nullable=False)


class Event(Base):
    id: Mapped[UUID] = mapped_column(Uuid, index=True, primary_key=True, default=uuid4)
    name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    place: Mapped[str] = mapped_column(String)
    organizer: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    description: Mapped[str] = mapped_column(Text, nullable=False)
    max_donors: Mapped[int] = mapped_column(Integer, nullable=False)
    registred: Mapped[int] = mapped_column(Integer, default=0)
    start_date: Mapped[datetime] = mapped_column(DateTime)
    end_date: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    registrations_list: Mapped[list["Registration"]] = relationship(
        back_populates="event", cascade="all, delete-orphan"
    )
    organizer_user: Mapped["User"] = relationship(back_populates="events")


class Registration(Base):
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    event_id: Mapped[UUID] = mapped_column(Uuid, ForeignKey("events.id", ondelete="CASCADE"))
    opened_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    closed: Mapped[bool] = mapped_column(Boolean, default=False)
    closed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    notification: Mapped[bool] = mapped_column(Boolean, default=True)

    user: Mapped["User"] = relationship(back_populates="registrations_list")
    event: Mapped["Event"] = relationship(back_populates="registrations_list")

class InfoForExcel(Base):
    id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    
    # Основные поля (добавляем surname и name)
    surname: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    patronymic: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    fullname: Mapped[str] = mapped_column(String, nullable=True)
    
    # Поля для данных из Excel
    group: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    donations_gavrilov: Mapped[int] = mapped_column(Integer, default=0)
    donations_fmba: Mapped[int] = mapped_column(Integer, default=0)
    last_donation_gavrilov: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    last_donation_fmba: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    social_media: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    donations: Mapped[int] = mapped_column(Integer, default=0)
    
    # Дополнительные поля
    birth_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    gender: Mapped[Gender] = mapped_column(Enum(Gender), default=Gender.UNDEFINED)
    university: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    weight: Mapped[int] = mapped_column(Integer, default=0)
    chronic_disease: Mapped[bool] = mapped_column(Boolean, default=False)
    medical_exemption: Mapped[bool] = mapped_column(Boolean, default=False)
    donor_earlier: Mapped[DonorEarlier] = mapped_column(Enum(DonorEarlier), default=DonorEarlier.YES)
    feedback: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    # user: Mapped["User"] = relationship(back_populates="info")