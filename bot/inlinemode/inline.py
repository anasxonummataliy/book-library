from aiogram import Router
from aiogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from bot.database.models import Book
from bot.database.base import db

inline_router = Router()
LIMIT = 50


@inline_router.inline_query()
async def get_inline_query(query: InlineQuery):
    text = query.query.strip()

    try:
        offset = int(query.offset) if query.offset else 0
    except ValueError:
        offset = 0

    if text:
        books: list[Book] = await Book.filter_startwith(
            db, text, limit=LIMIT, offset=offset
        )
    else:
        books: list[Book] = await Book.get_with_limit(limit=LIMIT, offset=offset)

    results = []
    for book in books:
        results.append(
            InlineQueryResultArticle(
                id=str(book.id),
                title=book.title,
                description=f"✍️ {book.author}",
                input_message_content=InputTextMessageContent(
                    message_text=f"kitob_{book.id}"  # ✅ botga shu yuboriladi
                ),
            )
        )

    next_offset = str(offset + LIMIT) if len(books) == LIMIT else ""
    await query.answer(results, cache_time=0, next_offset=next_offset)
