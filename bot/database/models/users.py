from typing import Optional
from datetime import datetime

from sqlalchemy import String, Boolean, BigInteger, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from bot.database.base import TimeBasedModel


class User(TimeBasedModel):
    __tablename__ = "users"

    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    first_name: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    username: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    is_blocked: Mapped[bool] = mapped_column(Boolean, default=False)
    last_activity: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return f"<User tg_id={self.tg_id} name={self.first_name}>"
