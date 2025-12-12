from sqlalchemy.orm import DeclarativeBase
from bot.database.session import async_engine

class Base(DeclarativeBase):
    pass