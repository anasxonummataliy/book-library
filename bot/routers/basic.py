from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

main_router = Router()


@main_router.message(CommandStart())
async def handle_message(message: Message):
    await message.answer("Bizning botimizga xush kelibsiz!")
