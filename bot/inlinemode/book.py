from aiogram import Router
from aiogram.utils.keyboard import InlineKeyboardBuilder

# from aiogram.utils.i18n import gettext as _
from aiogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)

from bot.database.models import Book
from bot.database.base import db


inline_router = Router()


@inline_router.inline_query()
async def get_inline_query(query: InlineQuery):
    results = []
    if len(query.query):
        books: list[Book] = await Book.filter_startwith(db, query.query)
    else:
        books: list[Book] = await Book.get_all()

    for book in books:
        ikm = InlineKeyboardBuilder()
        results.append(
            InlineQueryResultArticle(
                id=str(book.id),
                title=f"{book.title},\n",
                description=book.description,
                input_message_content=InputTextMessageContent(
                    message_text=f"{book.title}\n"
                ),
                reply_markup=ikm.as_markup(),
            )
        )

    await query.answer(results, cache_time=0)
