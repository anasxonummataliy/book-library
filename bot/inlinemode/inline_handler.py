from aiogram import Router
from aiogram.types import (
    InlineQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from bot.database.models import Book
from bot.database.base import db
from sqlalchemy import select, or_, func

inline_router = Router()

RESULTS_PER_PAGE = 10


def build_book_keyboard(book_id: int) -> InlineKeyboardBuilder:
    ikb = InlineKeyboardBuilder()
    ikb.row(
        InlineKeyboardButton(
            text="📥 Yuklab olish",
            callback_data=f"book:download:{book_id}",
        )
    )
    ikb.row(
        InlineKeyboardButton(
            text="🔍 Boshqa kitob qidirish",
            switch_inline_query_current_chat="",
        )
    )
    return ikb


def format_book_caption(book: Book) -> str:
    lines = [
        f"📚 <b>{book.title}</b>",
        f"✍️ <i>{book.author}</i>",
        f"{book.language_flag} Til: <b>{book.language.upper()}</b>",
    ]
    if book.description:
        lines.append(
            f"\n📝 {book.description[:300]}{'...' if len(book.description) > 300 else ''}"
        )
    lines.append(f"\n📦 Hajmi: <b>{book.file_size_mb}</b>")
    lines.append(f"📥 Yuklab olingan: <b>{book.download_count}</b> marta")
    return "\n".join(lines)


@inline_router.inline_query()
async def inline_book_search(query: InlineQuery):
    search_text = query.query.strip()
    offset = int(query.offset) if query.offset else 0

    if search_text:
        stmt = (
            select(Book)
            .where(
                or_(
                    Book.title.ilike(f"%{search_text}%"),
                    Book.author.ilike(f"%{search_text}%"),
                )
            )
            .order_by(Book.id.desc())
            .limit(RESULTS_PER_PAGE)
            .offset(offset)
        )
        count_stmt = select(func.count(Book.id)).where(
            or_(
                Book.title.ilike(f"%{search_text}%"),
                Book.author.ilike(f"%{search_text}%"),
            )
        )
    else:
        stmt = (
            select(Book).order_by(Book.id.desc()).limit(RESULTS_PER_PAGE).offset(offset)
        )
        count_stmt = select(func.count(Book.id))

    books = (await db.execute(stmt)).scalars().all()
    total_count = (await db.execute(count_stmt)).scalar() or 0

    results = []

    for book in books:

        # Chat ga book_{id} xabar tushadi — bot shu xabarni ushlab kitobni yuboradi
        result = InlineQueryResultArticle(
            id=str(book.id),
            title=f"📚 {book.title}",
            description=f"✍️ {book.author} | {book.language_flag} {book.language.upper()} | 📦 {book.file_size_mb}",
            input_message_content=InputTextMessageContent(
                message_text=f"book_{book.id}",
            ),
            thumbnail_url=f"https://via.placeholder.com/100x140/1a1a2e/ffffff?text=📚",
            thumbnail_width=100,
            thumbnail_height=140,
        )
        results.append(result)

    next_offset = (
        str(offset + RESULTS_PER_PAGE)
        if offset + RESULTS_PER_PAGE < total_count
        else ""
    )

    if not results:
        empty_result = InlineQueryResultArticle(
            id="no_results",
            title="😔 Hech narsa topilmadi",
            description=f"'{search_text}' bo'yicha kitob topilmadi",
            input_message_content=InputTextMessageContent(
                message_text=(
                    f"🔍 <b>'{search_text}'</b> bo'yicha hech qanday kitob topilmadi.\n\n"
                    "Qidiruv so'zini o'zgartirib ko'ring."
                ),
                parse_mode="HTML",
            ),
        )
        results.append(empty_result)
        next_offset = ""

    await query.answer(
        results=results,
        next_offset=next_offset,
        cache_time=10,
        is_personal=True,
    )
