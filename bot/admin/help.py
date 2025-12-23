from aiogram.types import BotCommand

from aiogram import Bot, Router, F
from aiogram.types import Message
from aiogram.filters import Command

from bot.filters.admin_filter import isAdmin
router = Router()

ADMIN_HELP_TEXT = """
<b>👑 Admin Panel — Buyruqlar ro‘yxati</b>

<b>/start</b> – Botni ishga tushirish 🏁
<b>/users</b> – Foydalanuvchilar ro‘yxati 📚
<b>/channels</b> – Majburiy kanallar ro‘yxati 📢
<b>/add_channel</b> – Majburiy kanal qo‘shish ➕
<b>/broadcast</b> – Barcha foydalanuvchilarga xabar yuborish 📣
<b>/reply</b> – Biror foydalanuvchiga xabar yuborish ✉️

<i>⚙️ Ushbu menyu faqat adminlar uchun mo‘ljallangan.</i>
"""


@router.message(Command("help"))
async def help_handler(message: Message):
    await message.answer(ADMIN_HELP_TEXT, parse_mode="HTML")
