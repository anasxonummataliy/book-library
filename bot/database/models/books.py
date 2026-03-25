from typing import Optional
from sqlalchemy import Integer, String, select
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncSession


from bot.database.base import BaseModel
from bot.repo.book_repo import BookRepository


class Book(BaseModel, BookRepository):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(300), nullable=False, index=True)
    author: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    cover_image_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    file_id: Mapped[str] = mapped_column(String(200), nullable=False, unique=True)
    file_size: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    language: Mapped[str] = mapped_column(String(10), default="en")
    description: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)

    @classmethod
    async def filter_startwith(
        cls, session, text: str, limit: int = 50, offset: int = 0
    ):
        result = await session.execute(
            select(cls).where(cls.title.ilike(f"{text}%")).limit(limit).offset(offset)
        )
        return result.scalars().all()

    @classmethod
    async def get_by_id(cls, session, book_id: int) -> "Book | None":
        return await session.get(cls, book_id)
