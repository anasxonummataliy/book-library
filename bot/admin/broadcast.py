import asyncio
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, User

router = Router()


@router.message(Command("broadcast"))
async def broadcast_handler(message: Message):
    users = await User.get_all()
    for user in users:
        try:
            await message.bot.send_message(
                user.tg_id, "Bu xabar barcha foydalanuvchilarga yuborilmoqda!"
            )
            await asyncio.sleep(0.1)
        except Exception as e:
            print(f"Xatolik yuz berdi: {e}")
