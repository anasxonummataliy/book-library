from aiogram.types import BotCommand

from aiogram import Bot, Router, F
from aiogram.enums import ChatType
from aiogram.types import Message
from aiogram.filters import Command, CommandStart

from bot.filters.admin_filter import isAdmin
from bot.config import channels_id

admin_commands = [
    BotCommand(command="/start", description="Boshlash🏁"),
    BotCommand(command="/users", description="User list📚"),
    BotCommand(command="/channels", description="Channel list📢"),
    BotCommand(command="/add_channel", description="Majburiy kanal qo'shish➕"),
    BotCommand(
        command="/broadcast", description="Hamma userlar uchun xabar yuborish📢"
    ),
    BotCommand(command="/reply", description="Bitta userga xabar yuborish"),
]

router = Router()
router.message.filter(isAdmin())

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
    await message.answer("Admin")
