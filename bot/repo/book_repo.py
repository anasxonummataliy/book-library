from sqlalchemy import select, delete
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

    async def get_all_books(self):
        query = select(Book)

        result = await self.db.execute(query)
        return result.scalars().all()

    async def delete_book(self, book_id: int):
        query = delete(Book).where(Book.id == book_id)

        await self.db.execute(query)
        await self.db.commit()
