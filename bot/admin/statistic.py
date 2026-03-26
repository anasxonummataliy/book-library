from datetime import datetime, date

from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from bot.database.models import User, Book

statistic_router = Router()


@statistic_router.message(Command("statistic"))
async def statistic_handler(message: Message):
    users = await User.get_all()
    books = await Book.get_all()

    total_users = len(users)
    today = date.today()
    new_today = sum(1 for u in users if u.created_at and u.created_at.date() == today)
    blocked = sum(1 for u in users if u.is_blocked)
    total_books = len(books)
    total_downloads = sum(b.download_count for b in books)

    text = (
        "📊 <b>Bot Statistikasi</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"👥 Jami foydalanuvchilar: <b>{total_users}</b>\n"
        f"🆕 Bugun qo'shilganlar: <b>{new_today}</b>\n"
        f"🚫 Bloklangan: <b>{blocked}</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"📚 Jami kitoblar: <b>{total_books}</b>\n"
        f"📥 Jami yuklashlar: <b>{total_downloads}</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"🕐 Vaqt: <b>{datetime.now().strftime('%d.%m.%Y %H:%M')}</b>"
    )
    await message.answer(text, parse_mode="HTML")


@statistic_router.callback_query(lambda c: c.data == "admin:stats")
async def stats_callback(callback: CallbackQuery):
    users = await User.get_all()
    books = await Book.get_all()

    total_users = len(users)
    today = date.today()
    new_today = sum(1 for u in users if u.created_at and u.created_at.date() == today)
    total_books = len(books)
    total_downloads = sum(b.download_count for b in books)

    text = (
        "📊 <b>Bot Statistikasi</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"👥 Jami foydalanuvchilar: <b>{total_users}</b>\n"
        f"🆕 Bugun qo'shilganlar: <b>{new_today}</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"📚 Jami kitoblar: <b>{total_books}</b>\n"
        f"📥 Jami yuklashlar: <b>{total_downloads}</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"🕐 Vaqt: <b>{datetime.now().strftime('%d.%m.%Y %H:%M')}</b>"
    )
    await callback.message.answer(text, parse_mode="HTML")
    await callback.answer()
