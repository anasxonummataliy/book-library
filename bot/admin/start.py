from aiogram.types import BotCommand
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

router = Router()


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


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Xush kelibsiz Admin!")


@router.message()
async def msg_handler(message: Message):
    await message.answer("Mavjud bo'lmagan commanda kiritdingiz!")
