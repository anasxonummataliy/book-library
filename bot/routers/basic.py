from aiogram import Router, Bot
from aiogram.types import Message, BotCommand
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from bot.database.models import User

main_router = Router()

user_commands = [
    BotCommand(command="/start", description="Boshlash 🏁"),
    BotCommand(command="/help", description="Yordam ❓"),
    BotCommand(command="/about", description="Bot haqida ℹ️"),
    BotCommand(command="/contact", description="Admin bilan bog'lanish ✉️"),
]


def start_keyboard():
    ikb = InlineKeyboardBuilder()
    ikb.row(
        InlineKeyboardButton(
            text="🔍 Kitob qidirish",
            switch_inline_query_current_chat="",
        )
    )
    return ikb.as_markup()


@main_router.message(CommandStart())
async def start_handler(message: Message):
    user = await User.get_with_tg_id(message.from_user.id)
    name = message.from_user.first_name or "Foydalanuvchi"

    if user is None:
        text = (
            f"👋 Assalomu alaykum, <b>{name}</b>!\n\n"
            "📚 <b>Kitob Kutubxonasiga xush kelibsiz!</b>\n\n"
            "Bu bot orqali minglab kitoblarni qidirib topishingiz va yuklab olishingiz mumkin.\n\n"
            "👇 Qidiruvni boshlash uchun tugmani bosing:"
        )
    else:
        text = (
            f"👋 Qaytib keldingiz, <b>{name}</b>!\n\n"
            "📚 Kitob qidirish uchun quyidagi tugmani bosing:"
        )

    await message.answer(text, parse_mode="HTML", reply_markup=start_keyboard())


@main_router.message(Command("about"))
async def about_handler(message: Message):
    text = (
        "📚 <b>Kitob Kutubxonasi</b>\n\n"
        "Bu bot orqali siz:\n"
        "• 🔍 Kitob nomi yoki muallif bo'yicha qidirish\n"
        "• 📥 Kitoblarni yuklab olish\n"
        "• 🌐 O'zbek, Rus va Ingliz tilidagi kitoblar\n\n"
        "❓ Yordam uchun /help buyrug'ini ishlating."
    )
    await message.answer(text, parse_mode="HTML")


@main_router.message(Command("help"))
async def help_handler(message: Message):
    text = (
        "❓ <b>Yordam</b>\n\n"
        "🔍 <b>Kitob qidirish:</b>\n"
        "Qidiruv tugmasini bosib, kitob nomi yoki muallifini yozing.\n\n"
        "📥 <b>Kitobni yuklab olish:</b>\n"
        "Natijadan kitobni tanlang va <i>Yuklab olish</i> tugmasini bosing.\n\n"
        "📖 <b>Navigatsiya:</b>\n"
        "◀️ Oldingi / Keyingi ▶️ tugmalari bilan kitoblar o'rtasida harakat qiling.\n\n"
        "✉️ Admin bilan bog'lanish: /contact"
    )
    await message.answer(text, parse_mode="HTML", reply_markup=start_keyboard())
