from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from bot.config import channels_id

router = Router()


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
