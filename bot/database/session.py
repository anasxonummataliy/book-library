import os
from functools import cache
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from bot.config import conf


@cache
def get_async_engine():
    db_path = conf.db.DB_PATH
    os.makedirs(
        os.path.dirname(db_path) if os.path.dirname(db_path) else ".", exist_ok=True
    )
    return create_async_engine(
        url=conf.db.db_url,
        connect_args={"check_same_thread": False},
        echo=False,
    )


@cache
def get_session_maker() -> async_sessionmaker[AsyncSession]:
    engine = get_async_engine()
    return async_sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False,
    )


@asynccontextmanager
async def get_async_session_context():
    session_maker = get_session_maker()
    async with session_maker() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
