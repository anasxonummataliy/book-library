from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from datetime import datetime, date
from bot.database.models import User

statistic_router = Router()


@statistic_router.message(Command("statistic"))
async def statistic_handler(message: Message):
    users = await User.get_all()
    total_users = len(users)

    today = date.today()
    new_today = sum(1 for u in users if u.created_at.date() == today)

    text = (
        "📊 <b>Bot statistikasi</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"👥 Jami foydalanuvchilar: <b>{total_users}</b>\n"
        f"🆕 Bugun qo'shilganlar: <b>{new_today}</b>\n"
        f"🕐 Yangilangan vaqt: <b>{datetime.now().strftime('%H:%M:%S')}</b>\n"
        "━━━━━━━━━━━━━━━━━━━━"
    )

    await message.answer(text, parse_mode="HTML")
