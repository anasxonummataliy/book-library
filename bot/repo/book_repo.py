from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models.books import Book


class BookRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_book(self, title: str, author: str, description: str):
        book = Book(title=title, author=author, description=description)
        self.db.add(book)
        await self.db.commit()
        await self.db.refresh(book)
        return book

    async def get_book(self, book_id: int):
        query = select(Book).where(Book.id == book_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def get_books_paginated(self, limit: int = 10, offset: int = 0):
        query = select(Book).limit(limit).offset(offset)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def count_books(self):
        from sqlalchemy import func

        query = select(func.count(Book.id))
        result = await self.db.execute(query)
        return result.scalar()

    async def delete_book(self, book_id: int):
        from sqlalchemy import delete

        query = delete(Book).where(Book.id == book_id)
        await self.db.execute(query)
        await self.db.commit()

    async def search_books(self, query_text: str, limit: int = 10, offset: int = 0):
        from sqlalchemy import or_

        query = (
            select(Book)
            .where(
                or_(
                    Book.title.ilike(f"%{query_text}%"),
                    Book.author.ilike(f"%{query_text}%"),
                )
            )
            .limit(limit)
            .offset(offset)
        )
        result = await self.db.execute(query)
        return result.scalars().all()
