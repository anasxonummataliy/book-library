import logging
from sqlalchemy import Column, DateTime, func, select, update, delete
from sqlalchemy.orm import DeclarativeBase, declared_attr, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncAttrs, AsyncSession


from bot.config import settings as conf


class AbstractClass:
    @classmethod
    async def commit(cls):
        try:
            await db.commit()
        except Exception as e:
            await db.rollback()
            logging.info(f"postgres commit error: {e}")

    async def get_all(cls):
        return (await db.execute(select(cls))).scalars().all()

    @classmethod
    async def get(cls, _id):
        return (await db.execute(select(cls).where(cls.id == _id))).scalar()

    @classmethod
    async def create(cls):
        pass

    @classmethod
    async def update(cls):
        pass


class Base(DeclarativeBase):
    @declared_attr
    def created_at(cls):
        return Column(DateTime, default=func.now())

    @declared_attr
    def updated_at(cls):
        return Column(DateTime, default=func.now(), onupdate=func.now())


class AsyncDatabaseSession:
    def __init__(self):
        self._session = None
        self._engine = None

    def __getattr__(self, name):
        return getattr(self._session, name)

    def init(self):
        self._engine = create_async_engine(conf.db_url)
        self._session = sessionmaker(
            self._engine, expire_on_commit=False, class_=AsyncSession
        )

    async def create_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all())

    async def drop_all(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all())


db = AsyncDatabaseSession()
db.init()
