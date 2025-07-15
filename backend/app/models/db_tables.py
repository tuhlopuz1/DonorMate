from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

import inflect
from app.models.schemas import DonorEarlier, Gender, Role
from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
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
    username: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    telegram_name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.DONOR)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    info: Mapped[Optional["Information"]] = relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan"
    )

    registrations_list: Mapped[list["Registration"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Information(Base):
    id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    fullname: Mapped[str] = mapped_column(String)
    surname: Mapped[str] = mapped_column(String)
    patronymic: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    birth_date: Mapped[datetime] = mapped_column(DateTime)
    gender: Mapped[Gender] = mapped_column(Enum(Gender), default=Gender.UNDEFINED)
    university: Mapped[str] = mapped_column(String, nullable=True)
    group: Mapped[str] = mapped_column(String, nullable=True)
    weight: Mapped[int] = mapped_column(Integer)
    chronic_disease: Mapped[bool] = mapped_column(Boolean)
    medical_exemption: Mapped[bool] = mapped_column(Boolean)
    donor_earlier: Mapped[DonorEarlier] = mapped_column(Enum(DonorEarlier), default=DonorEarlier.NO)
    feedback: Mapped[str] = mapped_column(String, nullable=True)

    user: Mapped["User"] = relationship(back_populates="info")


class MedicalExemption(Base):
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    start_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    end_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    medic_phone_num: Mapped[str] = mapped_column(String, nullable=True)
    comment: Mapped[str] = mapped_column(String, nullable=True)
    url: Mapped[str] = mapped_column(String, nullable=False)


class Event(Base):
    id: Mapped[UUID] = mapped_column(Uuid, index=True, primary_key=True, default=uuid4)
    name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    max_donors: Mapped[int] = mapped_column(Integer, nullable=False)
    registred: Mapped[int] = mapped_column(Integer, default=0)
    start_date: Mapped[datetime] = mapped_column(DateTime)
    end_date: Mapped[datetime] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    registrations_list: Mapped[list["Registration"]] = relationship(
        back_populates="event", cascade="all, delete-orphan"
    )


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
