
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("reply"))
async def reply_handler(message: Message):
    pass
