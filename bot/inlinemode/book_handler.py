from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, Message
from sqlalchemy import select

from bot.database.models import Book
from bot.database.base import db
from bot.inlinemode.inline_handler import format_book_caption, build_book_keyboard

book_router = Router()


async def send_book_by_id(message: Message, book_id: int):
    """Kitobni ID orqali topib, chiroyli ko'rinishda yuborish"""
    book = (
        await db.execute(select(Book).where(Book.id == book_id))
    ).scalar_one_or_none()

    if not book:
        await message.answer("❌ Kitob topilmadi.")
        return

    caption = format_book_caption(book)
    keyboard = build_book_keyboard(book.id)

    try:
        if book.cover_image_id:
            # Muqova bor — rasm + caption
            await message.answer_photo(
                photo=book.cover_image_id,
                caption=caption,
                parse_mode="HTML",
                reply_markup=keyboard.as_markup(),
            )
        else:
            # Muqova yo'q — faqat matn
            await message.answer(
                text=caption,
                parse_mode="HTML",
                reply_markup=keyboard.as_markup(),
            )
    except Exception as e:
        await message.answer(f"Xatolik: {str(e)[:100]}")


@book_router.message(F.text.regexp(r"^book_(\d+)$"))
async def book_id_message_handler(message: Message):
    """book_{id} xabarini ushlab kitobni yuboradi"""
    book_id = int(message.text.split("_")[1])
    await send_book_by_id(message, book_id)


@book_router.callback_query(F.data.startswith("book:download:"))
async def download_book_handler(callback: CallbackQuery):
    """Yuklab olish tugmasi — kitob faylini yuboradi"""
    book_id = int(callback.data.split(":")[2])

    book = (
        await db.execute(select(Book).where(Book.id == book_id))
    ).scalar_one_or_none()

    if not book:
        await callback.answer("Kitob topilmadi ❌", show_alert=True)
        return

    try:
        await callback.message.answer_document(
            document=book.file_id,
            caption=(
                f"📚 <b>{book.title}</b>\n"
                f"✍️ <i>{book.author}</i>\n"
                f"{book.language_flag} {book.language.upper()} | 📦 {book.file_size_mb}"
            ),
            parse_mode="HTML",
        )
        await Book.update(_id=book.id, download_count=book.download_count + 1)
        await callback.answer("📥 Kitob yuborildi!")
    except Exception as e:
        await callback.answer(f"Xatolik: {str(e)[:50]}", show_alert=True)


@book_router.callback_query(F.data == "book:noop")
async def noop_handler(callback: CallbackQuery):
    await callback.answer()
