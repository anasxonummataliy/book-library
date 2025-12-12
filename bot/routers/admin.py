from aiogram.types import BotCommand

from aiogram import Bot, Router, F
from aiogram.enums import ChatType
from aiogram.types import Message
from aiogram.filters import Command, CommandStart

from bot.filters.admin_filter import isAdmin
from bot.config import channels_id

admin_commands = [
    BotCommand(command="/start", description="Boshlash 🏁"),
    BotCommand(command="/users", description="Foydalanuvchilar haqida ma'lumot💽"),
    BotCommand(command="/channels", description="Kanallar ro‘yxati 📢"),
    BotCommand(command="/add_channel", description="Majburiy kanal qo‘shish ➕"),
    BotCommand(
        command="/broadcast", description="Barcha foydalanuvchilarga xabar yuborish 📣"
    ),
    BotCommand(command="/reply", description="Biror foydalanuvchiga javob qaytarish ✉️"),
    BotCommand(command="/help", description="Yordam ❓"),
]


router = Router()
router.message.filter(isAdmin())

@router.message(Command('users'))
async def get_users_data(message: Message):
    pass

@router.message(Command('channels'))
async def get_channels(message: Message):
    pass

@router.message(Command('reply'))
async def reply_handler(message: Message):
    pass

@router.message(Command("broadcast"))
async def broadcast_handler(message: Message):
    pass

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
    await message.answer(ADMIN_HELP_TEXT, parse_mode='HTML')

@router.message(Command("add_channel"))
async def add_channel_start(message: Message):
    await message.answer(
        "Botni kanalga admin qiling, keyin kanaldan xabar forward qiling"
    )

@router.message(F.forward_from_chat & (F.forward_from_chat.type == "channel"))
async def save_channel(message: Message):
    channel_id = message.forward_from_chat.id
    if channel_id not in channels_id:
        channels_id.append(channel_id)
        await message.answer(f"Kanal qo'shildi! ID: {channel_id}")
    else:
        await message.answer(f"Bu kanal allaqachon qo'shilgan!")

@router.message(CommandStart())  
async def start_handler(message: Message):
    await message.answer("Xush kelibsiz Admin!")

@router.message()
async def msg_handler(message: Message):
    await message.answer("Mavjud bo'lmagan commanda kiritdingiz!")
