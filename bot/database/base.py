from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from sqlalchemy import (
    and_,
    select,
    delete as sqlalchemy_delete,
    update as sqlalchemy_update, DateTime,
)

from bot.config import conf

class Base(AsyncAttrs, DeclarativeBase):
    pass


class AbstractClass:
    @staticmethod
    async def commit():
        try:
            await db.commit()
        except Exception as e:
            await db.rollback()

    @classmethod
    async def get_all(cls):
        return (await db.execute(select(cls))).scalars().all()

    @classmethod
    async def get(cls, _id):
        return await db.execute(select(cls).where(cls.id == _id)).scalar()

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
            raise

    @classmethod
    async def update(cls, _id, **kwargs):
        query = (
            sqlalchemy_update(cls)
            .where(cls.id == _id)
            .values(**kwargs)
            .execution_options(synchronize_session="fetch")
        )
        await db.execute(query)
        await cls.commit()

    @classmethod
    async def delete(cls, _id):
        query = sqlalchemy_delete(cls).where(cls.id == _id)
        await db.execute(query)
        await cls.commit()
        return (await db.execute(select(cls))).scalars()

    @classmethod
    async def filter(cls, **kwargs):
        conditions = [getattr(cls, key) == value for key, value in kwargs.items()]
        query = select(cls).where(and_(*conditions))
        return (await db.execute(query)).scalars().all()


class AsyncDatabaseSession:
    def __init__(self):
        self._engine = None
        self._session = None

    def __getattr__(self, name):
        return self._session, name

    def init(self):
        self._engine = create_async_engine(conf.db.db_url)
        self._session = sessionmaker(
            self._engine, expire_on_commit=False, class_=AsyncSession
        )()

    async def create_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def drop_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)


db = AsyncDatabaseSession()
db.init()


class BaseModel(AbstractClass, Base):
    __abstract__ = True


class TimeBasedModel(BaseModel):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
