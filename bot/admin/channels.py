from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.database.models import Channel

router = Router()


def channels_list_keyboard(channels):
    builder = InlineKeyboardBuilder()

    for channel in channels:
        title = channel.channel_title or str(channel.tg_id)
        builder.button(
            text=f"📢 {title}", callback_data=f"channel:view:{channel.tg_id}"
        )

    builder.adjust(1)
    return builder.as_markup()


def channel_detail_keyboard(channel_id: int):
    builder = InlineKeyboardBuilder()
    builder.button(text="🗑 O‘chirish", callback_data=f"channel:delete:{channel_id}")
    builder.button(text="⬅️ Orqaga", callback_data="channel:back")
    builder.adjust(1)
    return builder.as_markup()


def channels_list_text(channels):
    if not channels:
        return "Hozircha kanal qo‘shilmagan!"
    return "Kanallar ro‘yxati:\nQuyidagilardan birini tanlang."


def channel_detail_text(channel):
    return (
        f"📢 <b>{channel.channel_title}</b>\n"
        f"🆔 <code>{channel.tg_id}</code>\n"
        f"👤 @{channel.channel_username if channel.channel_username else 'yo‘q'}"
    )


@router.message(Command("channels"))
async def get_channels(message: Message):
    channels = await Channel.get_all()

    if not channels:
        await message.answer("Hozircha kanal qo‘shilmagan!")
        return

    await message.answer(
        text=channels_list_text(channels),
        reply_markup=channels_list_keyboard(channels),
    )


@router.message(Command("add_channel"))
async def add_channel_start(message: Message):
    await message.answer(
        "Botni kanalga admin qiling, keyin kanaldan xabar forward qiling."
    )


@router.message(F.forward_from_chat & (F.forward_from_chat.type == "channel"))
async def save_channel(message: Message):
    channel_id = message.forward_from_chat.id
    existing_channel = await Channel.get_with_tg_id(tg_id=channel_id)

    if existing_channel is not None:
        await message.answer("Bu kanal allaqachon qo‘shilgan!")
        return

    await Channel.create(
        tg_id=channel_id,
        channel_link=message.forward_from_chat.invite_link or None,
        channel_username=message.forward_from_chat.username or None,
        channel_title=message.forward_from_chat.title,
    )
    await message.answer(f"Kanal qo‘shildi! ID: {channel_id}")


@router.callback_query(F.data.startswith("channel:view:"))
async def channel_view_callback(callback: CallbackQuery):
    channel_id = int(callback.data.split(":")[2])
    channel = await Channel.get_with_tg_id(tg_id=channel_id)

    if channel is None:
        await callback.answer("Kanal topilmadi", show_alert=True)
        return

    await callback.message.edit_text(
        text=channel_detail_text(channel),
        parse_mode="HTML",
        reply_markup=channel_detail_keyboard(channel_id),
    )
    await callback.answer()


@router.callback_query(F.data == "channel:back")
async def channel_back_callback(callback: CallbackQuery):
    channels = await Channel.get_all()

    if not channels:
        await callback.message.edit_text("Hozircha kanal qo‘shilmagan!")
        await callback.answer()
        return

    await callback.message.edit_text(
        text=channels_list_text(channels),
        reply_markup=channels_list_keyboard(channels),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("channel:delete:"))
async def channel_delete_callback(callback: CallbackQuery):
    channel_id = int(callback.data.split(":")[2])
    channel = await Channel.get_with_tg_id(tg_id=channel_id)

    if channel is None:
        await callback.answer("Kanal topilmadi", show_alert=True)
        return

    channel_title = channel.channel_title or str(channel.tg_id)

    await Channel.delete(telegram_id=channel_id)

    channels = await Channel.get_all()

    if not channels:
        await callback.message.edit_text(
            f"✅ <b>{channel_title}</b> o‘chirildi.\n\nHozircha kanal qolmadi.",
            parse_mode="HTML",
        )
        await callback.answer("Kanal o‘chirildi")
        return

    await callback.message.edit_text(
        text=(
            f"✅ <b>{channel_title}</b> o‘chirildi.\n\n"
            f"Kanallar ro‘yxati:\nQuyidagilardan birini tanlang."
        ),
        parse_mode="HTML",
        reply_markup=channels_list_keyboard(channels),
    )
    await callback.answer("Kanal o‘chirildi")
