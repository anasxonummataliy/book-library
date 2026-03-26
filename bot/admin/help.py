from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

ADMIN_HELP = """
👑 <b>Admin Panel — Buyruqlar</b>

📚 <b>Kitoblar:</b>
<b>/start</b> → Panel va kitob qo'shish tugmasi

📢 <b>Kanallar:</b>
<b>/channels</b> → Kanallar ro'yxati
<b>/add_channel</b> → Kanal qo'shish

📊 <b>Statistika:</b>
<b>/statistic</b> → Foydalanuvchilar statistikasi

📣 <b>Xabar yuborish:</b>
<b>/broadcast</b> → Barchaga xabar yuborish

✉️ <b>Javob berish:</b>
Foydalanuvchi xabariga reply qiling — avtomatik jo'natiladi.

<i>⚙️ Faqat admin uchun</i>
"""


@router.message(Command("help"))
async def admin_help(message: Message):
    await message.answer(ADMIN_HELP, parse_mode="HTML")
