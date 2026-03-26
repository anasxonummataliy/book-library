import os
import logging
from typing import Optional
from datetime import datetime

from sqlalchemy.orm.attributes import Mapped
from sqlalchemy.types import DateTime
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncAttrs,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.orm import DeclarativeBase, declared_attr, mapped_column
from sqlalchemy import (
    Integer,
    and_,
    select,
    delete as sqlalchemy_delete,
    update as sqlalchemy_update,
)

from bot.config import conf


class Base(AsyncAttrs, DeclarativeBase):
    @declared_attr.directive
    def __tablename__(cls) -> str:
        name = cls.__name__
        result = ""
        for i, char in enumerate(name):
            if char.isupper() and i != 0:
                result += "_"
            result += char.lower()
        if result.endswith("y"):
            result = result[:-1] + "ie"
        return result + "s"


class AsyncDatabaseSession:
    def __init__(self):
        self._session: Optional[AsyncSession] = None
        self._engine = None

    def __getattr__(self, name):
        return getattr(self._session, name)

    def init(self):
        # SQLite uchun data papkasini yaratish
        db_path = conf.db.DB_PATH
        os.makedirs(
            os.path.dirname(db_path) if os.path.dirname(db_path) else ".", exist_ok=True
        )

        self._engine = create_async_engine(
            conf.db.db_url,
            echo=False,
            connect_args={"check_same_thread": False},  # SQLite uchun zarur
        )
        self._session = async_sessionmaker(
            self._engine,
            expire_on_commit=False,
            class_=AsyncSession,
        )()

    async def create_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


db = AsyncDatabaseSession()
db.init()


class AbstractClass:
    @staticmethod
    async def commit():
        try:
            await db.commit()
        except Exception as e:
            await db.rollback()
            logging.error(f"DB commit error: {e}")

    @classmethod
    async def get_all(cls):
        return (await db.execute(select(cls))).scalars().all()

    @classmethod
    async def get_with_limit(cls, limit: int, offset: int):
        return (
            (await db.execute(select(cls).limit(limit).offset(offset))).scalars().all()
        )

    @classmethod
    async def get(cls, _id: int):
        return (await db.execute(select(cls).where(cls.id == _id))).scalar()

    @classmethod
    async def get_with_tg_id(cls, tg_id: int):
        return (await db.execute(select(cls).where(cls.tg_id == tg_id))).scalar()

    @classmethod
    async def create(cls, **kwargs):
        try:
            obj = cls(**kwargs)
            db.add(obj)
            await cls.commit()
            await db.refresh(obj)
            return obj
        except Exception as e:
            await db.rollback()
            logging.error(f"create error: {e}")
            raise

    @classmethod
    async def update(
        cls,
        _id: Optional[int] = None,
        telegram_id: Optional[int] = None,
        **kwargs,
    ):
        if _id is not None:
            query = (
                sqlalchemy_update(cls)
                .where(cls.id == _id)
                .values(**kwargs)
                .execution_options(synchronize_session="fetch")
            )
        else:
            query = (
                sqlalchemy_update(cls)
                .where(cls.tg_id == telegram_id)
                .values(**kwargs)
                .execution_options(synchronize_session="fetch")
            )
        await db.execute(query)
        await cls.commit()

    @classmethod
    async def delete(
        cls,
        _id: Optional[int] = None,
        telegram_id: Optional[int] = None,
    ):
        if _id is not None:
            query = sqlalchemy_delete(cls).where(cls.id == _id)
        else:
            query = sqlalchemy_delete(cls).where(cls.tg_id == telegram_id)
        await db.execute(query)
        await cls.commit()

    @classmethod
    async def filter(cls, **kwargs):
        conditions = [getattr(cls, key) == value for key, value in kwargs.items()]
        query = select(cls).where(and_(*conditions))
        return (await db.execute(query)).scalars().all()

    @classmethod
    async def filter_one(cls, **kwargs):
        conditions = [getattr(cls, key) == value for key, value in kwargs.items()]
        query = select(cls).where(and_(*conditions))
        return (await db.execute(query)).scalar_one_or_none()

    async def save_model(self):
        db.add(self)
        await self.commit()
        await db.refresh(self)
        return self


class BaseModel(Base, AbstractClass):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


class TimeBasedModel(BaseModel):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )
