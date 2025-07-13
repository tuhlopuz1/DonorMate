from datetime import datetime
import inflect
from typing import Optional
from sqlalchemy import String, DateTime, BigInteger
from sqlalchemy.orm import declarative_base, declared_attr, Mapped, mapped_column

p = inflect.engine()


class Base:
    @declared_attr
    def __tablename__(cls):
        return p.plural(cls.__name__.lower())


Base = declarative_base(cls=Base)


class User(Base):
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    telegram_name: Mapped[str] = mapped_column(String, nullable=True)
    fullname: Mapped[str] = mapped_column(String, nullable=True)
    surname: Mapped[str] = mapped_column(String, nullable=True)
    patronymic: Mapped[str] = mapped_column(String, nullable=True)
    birth_date: Mapped[datetime] = mapped_column(DateTime, nullable=True)
