from aiogram import Router, F
from aiogram.types import Message
from bot.database.models import Book
from bot.database.base import db

book_router = Router()


@book_router.message(F.text.regexp(r"^kitob_\d+$"))
async def handle_book_message(message: Message):
    book_id = int(message.text.split("_")[1])

    book: Book | None = await Book.get_by_id(db, book_id)

    if not book:
        await message.answer("❌ Kitob topilmadi!")
        return

    size_text = ""
    if book.file_size:
        size_mb = round(book.file_size / 1024 / 1024, 2)
        size_text = f"\n📦 {size_mb} MB"

    caption = (
        f"📚 *{book.title}*\n"
        f"✍️ _{book.author}_\n"
        f"🌐 {book.language.upper()}"
        f"{size_text}\n\n"
        f"{book.description or ''}"
    )

    if book.cover_image_id:
        await message.answer_photo(
            photo=book.cover_image_id, caption=caption, parse_mode="Markdown"
        )
    else:
        await message.answer(caption, parse_mode="Markdown")

    await message.answer_document(
        document=book.file_id, caption=f"📥 *{book.title}*", parse_mode="Markdown"
    )
