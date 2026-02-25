from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.repo import BookRepository
from bot.database.base import db

books_router = Router()

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

BOOKS_PER_PAGE = 10


@books_router.message(Command("books"))
async def books_handler(message: Message):

    repo = BookRepository(db)
    page = 0
    offset = page * BOOKS_PER_PAGE

    books = await repo.get_books_paginated(limit=BOOKS_PER_PAGE, offset=offset)

    if not books:
        await message.answer("Kitob topilmadi ❌")
        return

    kb = InlineKeyboardBuilder()

    for book in books:
        kb.button(text=f"{book.title} — {book.author}", callback_data=f"book_{book.id}")

    # ✅ Next button
    kb.button(text="Keyingi ➡️", callback_data=f"books_page_{page+1}")

    kb.adjust(1)
    await message.answer("📚 Kitoblar ro‘yxati:", reply_markup=kb.as_markup())


@books_router.callback_query(F.data.startswith("books_page_"))
async def books_pagination_handler(callback: CallbackQuery):

    page = int(callback.data.split("_")[-1])
    offset = page * BOOKS_PER_PAGE

    repo = BookRepository(db)
    books = await repo.get_books_paginated(limit=BOOKS_PER_PAGE, offset=offset)

    if not books:
        await callback.answer("Boshqa kitob yo‘q ❌", show_alert=True)
        return

    kb = InlineKeyboardBuilder()

    for book in books:
        kb.button(text=f"{book.title} — {book.author}", callback_data=f"book_{book.id}")

    if page > 0:
        kb.button(text="⬅️ Oldingi", callback_data=f"books_page_{page-1}")

    kb.button(text="Keyingi ➡️", callback_data=f"books_page_{page+1}")

    kb.adjust(1)

    await callback.message.edit_reply_markup(reply_markup=kb.as_markup())
    await callback.answer()
