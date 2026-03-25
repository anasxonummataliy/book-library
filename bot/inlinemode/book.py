from aiogram import Router
from aiogram.utils.keyboard import InlineKeyboardBuilder
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

    # Offsetni olish
    try:
        offset = int(query.offset) if query.offset else 0
    except ValueError:
        offset = 0

    # DBdan olish (limit + offset bilan)
    if text:
        books: list[Book] = await Book.filter_startwith(
            db, text, limit=LIMIT, offset=offset
        )
    else:
        books: list[Book] = await Book.get_with_limit(limit=LIMIT, offset=offset)

    results = []
    for book in books:
        ikm = InlineKeyboardBuilder()
        # ... tugmalarni shu yerga qo'shing

        results.append(
            InlineQueryResultArticle(
                id=str(book.id),
                title=book.title,
                description=book.description,
                input_message_content=InputTextMessageContent(
                    message_text=f"📚 *{book.title}*", parse_mode="Markdown"
                ),
                reply_markup=ikm.as_markup(),
            )
        )

    next_offset = str(offset + LIMIT) if len(books) == LIMIT else ""

    await query.answer(results, cache_time=0, next_offset=next_offset)
