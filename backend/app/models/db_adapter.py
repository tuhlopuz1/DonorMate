import logging
from typing import Any, List

from app.core.config import DATABASE_URL
from app.models.db_tables import Base
from sqlalchemy import func, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.future import select
from sqlalchemy.sql import and_

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AsyncDatabaseAdapter:
    def __init__(self, database_url: str = DATABASE_URL) -> None:
        self.engine = create_async_engine(
            database_url,
            echo=False,
            future=True,
        )
        self.SessionLocal = async_sessionmaker(bind=self.engine, class_=AsyncSession, expire_on_commit=False)

    async def initialize_tables(self) -> None:
        logger.info("Tables are created or exists")
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def get_all(self, model) -> List[Any]:
        async with self.SessionLocal() as session:
            result = await session.execute(select(model))
            return result.scalars().all()

    async def get_by_id(self, model, id) -> Any:
        async with self.SessionLocal() as session:
            result = await session.execute(select(model).where(model.id == id))
            return result.scalar_one_or_none()

    async def get_by_value(self, model, parameter: str, parameter_value: Any) -> List[Any]:
        async with self.SessionLocal() as session:
            result = await session.execute(select(model).where(getattr(model, parameter) == parameter_value))
            return result.scalars().all()

    async def get_by_values(self, model, conditions: dict) -> List[Any]:
        async with self.SessionLocal() as session:
            query = select(model)
            for key, value in conditions.items():
                query = query.where(getattr(model, key) == value)
            result = await session.execute(query)
            return result.scalars().all()

    async def insert(self, model, insert_dict: dict) -> Any:
        async with self.SessionLocal() as session:
            record = model(**insert_dict)
            session.add(record)
            await session.commit()
            await session.refresh(record)
            return record

    async def update_by_id(self, model, record_id: int, updates: dict):
        async with self.SessionLocal() as session:
            stmt = update(model).where(model.id == record_id).values(**updates)
            await session.execute(stmt)
            await session.commit()

    async def update_by_value(self, model, filters: dict, updates: dict):
        async with self.SessionLocal() as session:
            conditions = [getattr(model, key) == value for key, value in filters.items()]
            stmt = update(model).where(and_(*conditions)).values(**updates)
            await session.execute(stmt)
            await session.commit()

    async def delete(self, model, id: int) -> Any:
        async with self.SessionLocal() as session:
            result = await session.execute(select(model).where(model.id == id))
            record = result.scalar_one_or_none()
            if record:
                await session.delete(record)
                await session.commit()
            return record

    async def delete_by_value(self, model, parameter: str, parameter_value: Any) -> List[Any]:
        async with self.SessionLocal() as session:
            result = await session.execute(select(model).where(getattr(model, parameter) == parameter_value))
            records = result.scalars().all()
            for record in records:
                await session.delete(record)
            await session.commit()
            return records

    async def get_all_with_join(
        self, parent_model, child_model, parent_column_name: str, isouter: bool = True
    ) -> List[Any]:
        async with self.SessionLocal() as session:
            result = await session.execute(
                select(parent_model, child_model).join(
                    child_model,
                    getattr(parent_model, parent_column_name) == getattr(child_model, parent_column_name),
                    isouter=isouter,
                )
            )
            return result.all()

    async def get_by_id_with_join(
        self, parent_model, child_model, parent_id: int, parent_column_name: str, isouter: bool = True
    ) -> Any:
        async with self.SessionLocal() as session:
            result = await session.execute(
                select(parent_model, child_model)
                .join(
                    child_model,
                    getattr(parent_model, parent_column_name) == getattr(child_model, parent_column_name),
                    isouter=isouter,
                )
                .where(getattr(parent_model, "id") == parent_id)
            )
            return result.scalar_one_or_none()

    async def get_by_value_with_join(
        self,
        parent_model,
        child_model,
        parameter: str,
        parameter_value: Any,
        parent_column_name: str,
        isouter: bool = True,
    ) -> List[Any]:
        async with self.SessionLocal() as session:
            result = await session.execute(
                select(parent_model, child_model)
                .join(
                    child_model,
                    getattr(parent_model, parent_column_name) == getattr(child_model, parent_column_name),
                    isouter=isouter,
                )
                .where(getattr(parent_model, parameter) == parameter_value)
            )
            return result.all()

    async def get_count(self, model, conditions: dict = None) -> int:
        async with self.SessionLocal() as session:
            query = select(func.count()).select_from(model)
            if conditions:
                for key, value in conditions.items():
                    query = query.where(getattr(model, key) == value)
            result = await session.execute(query)
            return result.scalar()

    async def get_count_cond(self, model, *conditions) -> int:
        async with self.SessionLocal() as session:
            query = select(func.count()).select_from(model)
            if conditions:
                for i in range(0, len(conditions), 3):
                    column_name = conditions[i]
                    value = conditions[i + 1]
                    operator = conditions[i + 2]

                    column = getattr(model, column_name)

                    if operator == ">":
                        query = query.where(column > value)
                    elif operator == "<":
                        query = query.where(column < value)
                    elif operator == ">=":
                        query = query.where(column >= value)
                    elif operator == "<=":
                        query = query.where(column <= value)
                    elif operator == "==":
                        query = query.where(column == value)
                    elif operator == "!=":
                        query = query.where(column != value)
                    else:
                        raise ValueError(f"Unsupported operator: {operator}")
            result = await session.execute(query)
            return result.scalar()

    async def get_column_sum(self, model, column_name: str) -> int:
        async with self.SessionLocal() as session:
            result = await session.execute(select(func.sum(getattr(model, column_name))).select_from(model))
            return result.scalar()


adapter = AsyncDatabaseAdapter()
