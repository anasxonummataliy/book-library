from typing import Optional
from sqlalchemy import String, BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from bot.database.base import TimeBasedModel


class Channel(TimeBasedModel):
    __tablename__ = "channels"

    tg_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    channel_title: Mapped[str] = mapped_column(String(256), nullable=False)
    channel_username: Mapped[Optional[str]] = mapped_column(String(64), nullable=True)
    channel_link: Mapped[Optional[str]] = mapped_column(String(256), nullable=True)

    def __repr__(self) -> str:
        return f"<Channel id={self.tg_id} title={self.channel_title}>"
