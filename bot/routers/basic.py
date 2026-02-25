from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.types import BotCommand
from aiogram.types import BotCommandScopeChat

main_router = Router()


user_commands = [
    BotCommand(command="/start", description="Boshlash 🏁"),
    BotCommand(command="/search", description="Kitob qidirish 🔎"),
    BotCommand(command="/books", description="Barcha kitoblarni ko‘rish 📚"),
    BotCommand(command="/help", description="Yordam ❓"),
    BotCommand(command="/about", description="Bot haqida ℹ️"),
    BotCommand(command="/contact", description="Admin bilan bog‘lanish ✉️"),
]


@main_router.message(CommandStart())
async def handle_message(message: Message, bot: Bot):
    await bot.set_my_commands(
        user_commands, BotCommandScopeChat(chat_id=message.chat.id)
    )
    await message.answer("Bizning botimizga xush kelibsiz!")


@main_router.message(Command("about"))
async def about_handler(message: Message):
    about_text = (
        "📚 <b>Kitob kutubxonasi botiga xush kelibsiz!</b>\n\n"
        "Bu bot orqali siz turli janrlardagi kitoblarni qidirishingiz, "
        "ular haqida ma'lumot olishingiz va o'qish uchun havolalarni topishingiz mumkin.\n\n"
        "🔍 Kitob qidirish uchun /search buyrug'ini ishlating.\n"
        "❓ Yordam uchun /help buyrug'ini ishlating."
    )
    await message.answer(about_text, parse_mode="HTML")


@main_router.message(Command("help"))
async def help_handler(message: Message):
    help_text = (
        "❓ <b>Yordam</b>\n\n"
        "Bu bot orqali siz kitoblarni qidirishingiz va o'qish uchun havolalarni topishingiz mumkin.\n\n"
        "🔍 Kitob qidirish uchun /search buyrug'ini ishlating.\n"
        "ℹ️ Bot haqida ma'lumot olish uchun /about buyrug'ini ishlating.\n"
        "✉️ Admin bilan bog‘lanish uchun /contact buyrug'ini ishlating."
    )
    await message.answer(help_text, parse_mode="HTML")

