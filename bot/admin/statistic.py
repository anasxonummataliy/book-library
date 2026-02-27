from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.database.models import User

statistic_router = Router()


@statistic_router.message(Command("statistic"))
async def statistic_handler(message: Message):
    users = await User.get_all()
    total_users = len(users)

    text = (
        "📊 <b>Bot statistikasi</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        f"👥 Jami foydalanuvchilar: <b>{total_users}</b>\n"
        "━━━━━━━━━━━━━━━━━━━━"
    )

    await message.answer(text, parse_mode="HTML")
