
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

main_router = Router()

@main_router.message(CommandStart("main"))
async def handle_message(message):
    await message.answer("Hello from main router!")
