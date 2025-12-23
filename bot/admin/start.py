
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    await message.answer("Xush kelibsiz Admin!")


@router.message()
async def msg_handler(message: Message):
    await message.answer("Mavjud bo'lmagan commanda kiritdingiz!")
