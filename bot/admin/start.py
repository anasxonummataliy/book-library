from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

router = Router()


def admin_keyboard():
    ikb = InlineKeyboardBuilder()
    ikb.row(
        InlineKeyboardButton(text="📚 Kitob qo'shish", callback_data="add_book"),
        InlineKeyboardButton(text="🔍 Qidirish", switch_inline_query_current_chat=""),
    )
    ikb.row(
        InlineKeyboardButton(text="📊 Statistika", callback_data="admin:stats"),
        InlineKeyboardButton(text="📢 Kanallar", callback_data="admin:channels"),
    )
    return ikb.as_markup()


@router.message(CommandStart())
async def admin_start(message: Message):
    await message.answer(
        "👑 <b>Admin Panel</b>\n\n"
        "Xush kelibsiz! Quyidagi buyruqlardan foydalaning:\n\n"
        "📚 /add_channel — Kanal qo'shish\n"
        "📊 /statistic — Statistika\n"
        "📣 /broadcast — Xabar yuborish\n"
        "📢 /channels — Kanallar ro'yxati\n"
        "❓ /help — Yordam",
        parse_mode="HTML",
        reply_markup=admin_keyboard(),
    )
