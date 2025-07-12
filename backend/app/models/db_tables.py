import inflect
from sqlalchemy import Integer
from sqlalchemy.orm import declarative_base, declared_attr, Mapped, mapped_column

p = inflect.engine()


class Base:
    @declared_attr
    def __tablename__(cls):
        return p.plural(cls.__name__.lower())


Base = declarative_base(cls=Base)


class User(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
