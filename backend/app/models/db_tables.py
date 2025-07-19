from datetime import date, datetime
from typing import Optional
from uuid import UUID, uuid4

import inflect
from app.models.schemas import NotificationEnum, Place, Role, UserClass
from sqlalchemy import (
    TIMESTAMP,
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
    phone: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    role: Mapped[Role] = mapped_column(Enum(Role), default=Role.DONOR)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    notifications_bool: Mapped[bool] = mapped_column(Boolean, default=True)

    info: Mapped[Optional["Information"]] = relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan"
    )

    registrations_list: Mapped[list["Registration"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Information(Base):
    id: Mapped[Optional[int]] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="SET NULL"))
    phone: Mapped[int] = mapped_column(BigInteger, nullable=True)
    fsp: Mapped[str] = mapped_column(String, primary_key=True)
    group: Mapped[str] = mapped_column(String, nullable=True)
    user_class: Mapped[UserClass] = mapped_column(Enum(UserClass), default=UserClass.STU)
    social: Mapped[str] = mapped_column(String, nullable=True)
    donations_fmba: Mapped[int] = mapped_column(Integer, default=0)
    donations_gaur: Mapped[int] = mapped_column(Integer, default=0)
    last_don_fmba: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    last_don_gaur: Mapped[datetime] = mapped_column(DateTime, nullable=True)

    user: Mapped[Optional["User"]] = relationship(back_populates="info", uselist=False)


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
    place: Mapped[Place] = mapped_column(Enum(Place))
    description: Mapped[str] = mapped_column(Text, nullable=False)
    registred: Mapped[int] = mapped_column(Integer, default=0)
    start_date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    end_date: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
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
    accepted: Mapped[bool] = mapped_column(Boolean, default=False)
    notification: Mapped[bool] = mapped_column(Boolean, default=True)

    user: Mapped["User"] = relationship(back_populates="registrations_list")
    event: Mapped["Event"] = relationship(back_populates="registrations_list")


class Notification(Base):
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    type: Mapped[NotificationEnum] = mapped_column(
        Enum(NotificationEnum), nullable=False, default=NotificationEnum.INFO
    )
    date_to_valid: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=True)


class Question(Base):
    id: Mapped[UUID] = mapped_column(Uuid, primary_key=True, default=uuid4)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("users.id", ondelete="CASCADE"))
    question: Mapped[str] = mapped_column(String, nullable=False)
