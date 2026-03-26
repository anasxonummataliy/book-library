from sqlalchemy import select, or_, func
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models.books import Book


class BookRepository:

    @classmethod
    async def add_book(
        cls,
        db: AsyncSession,
        title: str,
        author: str,
        language: str,
        description: str | None = None,
        cover_image_id: str | None = None,
        file_id: str = "",
        file_size: int | None = None,
    ) -> Book:
        book = Book(
            title=title,
            author=author,
            language=language,
            description=description,
            cover_image_id=cover_image_id,
            file_id=file_id,
            file_size=file_size,
        )
        db.add(book)
        await db.commit()
        await db.refresh(book)
        return book

    @classmethod
    async def get_book(cls, db: AsyncSession, book_id: int) -> Book | None:
        result = await db.execute(select(Book).where(Book.id == book_id))
        return result.scalar_one_or_none()

    @classmethod
    async def get_books_paginated(
        cls, db: AsyncSession, limit: int = 10, offset: int = 0
    ) -> list[Book]:
        result = await db.execute(
            select(Book).order_by(Book.id.desc()).limit(limit).offset(offset)
        )
        return result.scalars().all()

    @classmethod
    async def count_books(cls, db: AsyncSession) -> int:
        result = await db.execute(select(func.count(Book.id)))
        return result.scalar() or 0

    @classmethod
    async def delete_book(cls, db: AsyncSession, book_id: int) -> None:
        from sqlalchemy import delete

        await db.execute(delete(Book).where(Book.id == book_id))
        await db.commit()

    @classmethod
    async def search_books(
        cls,
        db: AsyncSession,
        query_text: str,
        limit: int = 10,
        offset: int = 0,
    ) -> list[Book]:
        result = await db.execute(
            select(Book)
            .where(
                or_(
                    Book.title.ilike(f"%{query_text}%"),
                    Book.author.ilike(f"%{query_text}%"),
                )
            )
            .order_by(Book.id.desc())
            .limit(limit)
            .offset(offset)
        )
        return result.scalars().all()
