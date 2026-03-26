from typing import Optional
from sqlalchemy import String, Text, BigInteger, Integer
from sqlalchemy.orm import Mapped, mapped_column

from bot.database.base import TimeBasedModel


class Book(TimeBasedModel):
    __tablename__ = "books"

    title: Mapped[str] = mapped_column(String(256), nullable=False)
    author: Mapped[str] = mapped_column(String(256), nullable=False)
    language: Mapped[str] = mapped_column(String(8), default="uz")
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    cover_image_id: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    file_id: Mapped[str] = mapped_column(String(512), nullable=False)
    file_size: Mapped[Optional[int]] = mapped_column(BigInteger, nullable=True)
    download_count: Mapped[int] = mapped_column(Integer, default=0)

    def __repr__(self) -> str:
        return f"<Book id={self.id} title={self.title}>"

    @property
    def language_flag(self) -> str:
        flags = {"uz": "🇺🇿", "ru": "🇷🇺", "en": "🇬🇧"}
        return flags.get(self.language, "🌐")

    @property
    def file_size_mb(self) -> str:
        if self.file_size:
            return f"{self.file_size / (1024 * 1024):.1f} MB"
        return "Noma'lum"
