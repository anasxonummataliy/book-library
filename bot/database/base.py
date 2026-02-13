from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import DeclarativeBase, declared_attr, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncAttrs, AsyncSession


from bot.config import settings as conf


class Base(DeclarativeBase):
    @declared_attr
    def created_at(cls):
        return Column(DateTime, default=func.now())

    @declared_attr
    def updated_at(cls):
        return Column(DateTime, default=func.now(), onupdate=func.now())


class AsyncDatabseSession:
    def __init__(self):
        self._session = None
        self._engine = None

    def __getattr__(self, name):
        return getattr(self._session, name)

    def init(self):
        self._engine = create_async_engine(conf.db_url)
        self._session = sessionmaker(
            self._engine,
        )
