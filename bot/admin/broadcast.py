from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()

@router.message(Command("broadcast"))
async def broadcast_handler(message: Message):
    pass
