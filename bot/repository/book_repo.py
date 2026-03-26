from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class BookRepository:
    @classmethod
    async def add_book(
        cls, db: AsyncSession, title: str, author: str, description: str
    ):
        book = cls(title=title, author=author, description=description)
        db.add(book)
        await db.commit()
        await db.refresh(book)
        return book

    @classmethod
    async def get_book(cls, db: AsyncSession, book_id: int):
        query = select(cls).where(cls.id == book_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def get_books_paginated(
        cls, db: AsyncSession, limit: int = 10, offset: int = 0
    ):
        query = select(cls).limit(limit).offset(offset)
        result = await db.execute(query)
        return result.scalars().all()

    @classmethod
    async def count_books(cls, db: AsyncSession):
        from sqlalchemy import func

        query = select(func.count(cls.id))
        result = await db.execute(query)
        return result.scalar()

    @classmethod
    async def delete_book(cls, db: AsyncSession, book_id: int):
        from sqlalchemy import delete

        query = delete(cls).where(cls.id == book_id)
        await db.execute(query)
        await db.commit()

    @classmethod
    async def search_books(
        cls, db: AsyncSession, query_text: str, limit: int = 10, offset: int = 0
    ):
        from sqlalchemy import or_

        query = (
            select(cls)
            .where(
                or_(
                    cls.title.ilike(f"%{query_text}%"),
                    cls.author.ilike(f"%{query_text}%"),
                )
            )
            .limit(limit)
            .offset(offset)
        )
        result = await db.execute(query)
        return result.scalars().all()
