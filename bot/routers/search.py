from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command

from bot.repo import BookRepository
from bot.database.models import Book
from bot.database.base import db

search_router = Router()


class SearchBook(StatesGroup):
    waiting_for_query = State()


@search_router.message(Command("search"))
async def search_command(message: Message, state: FSMContext):

    await message.answer("🔎 Kitob nomini kiriting:")

    await state.set_state(SearchBook.waiting_for_query)


@search_router.message(SearchBook.waiting_for_query, F.text)
async def process_search(message: Message, state: FSMContext):

    query = message.text

    books: list[Book] = await Book().search_books(db, query)

    if not books:
        await message.answer("Kitob topilmadi ❌")
        return

    kb = InlineKeyboardBuilder()

    for book in books[:10]:  # limit
        kb.button(text=f"{book.title} — {book.author}", callback_data=f"book_{book.id}")

    kb.adjust(1)

    await message.answer("📚 Natijalar:", reply_markup=kb.as_markup())

    await state.clear()


@search_router.callback_query(F.data.startswith("book_"))
async def book_details(callback: CallbackQuery):

    book_id = int(callback.data.split("_")[1])

    book: Book = await Book().get_book(db, book_id)

    text = (
        f"📖 <b>{book.title}</b>\n"
        f"👤 {book.author}\n"
        "━━━━━━━━━━━━━━━\n"
        f"{book.description}"
    )

    await callback.message.answer(text, parse_mode="HTML")
    await callback.answer()
