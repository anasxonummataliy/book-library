from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

from bot.database.models import Channel

router = Router()


@router.message(Command("channels"))
async def get_channels(message: Message):
    channels = await Channel.get_all()
    if not channels:
        await message.answer("Hozircha kanal qo'shilmagan!")
        return
    channel_list = "\n\n".join(
        [
            f"━━━━━━━━━━━━━━━\n"
            f"📢 <b>{c.channel_title}</b>\n"
            f"🆔 <code>{c.tg_id}</code>\n"
            f"👤 @{c.channel_username if c.channel_username else 'yo‘q'}"
            for c in channels
        ]
    )
    await message.answer(f"Kanallar ro'yxati:\n{channel_list}", parse_mode="HTML")


@router.message(Command("add_channel"))
async def add_channel_start(message: Message):
    await message.answer(
        "Botni kanalga admin qiling, keyin kanaldan xabar forward qiling"
    )


@router.message(F.forward_from_chat & (F.forward_from_chat.type == "channel"))
async def save_channel(message: Message):
    channel_id = message.forward_from_chat.id
    channels = await Channel.get_with_tg_id(tg_id=channel_id)
    if channels is not None:
        await message.answer(f"Bu kanal allaqachon qo'shilgan!")
        return
    await Channel.create(
        tg_id=channel_id,
        channel_link=message.forward_from_chat.invite_link or None,
        channel_username=message.forward_from_chat.username or None,
        channel_title=message.forward_from_chat.title,
    )
    await message.answer(f"Kanal qo'shildi! ID: {channel_id}")
