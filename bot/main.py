import os
import sys
import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommandScopeAllPrivateChats, BotCommandScopeChat
from dotenv import load_dotenv

from bot.admin import admin_router
from bot.admin.commands import admin_commands
from bot.routers import user_router, user_commands
from bot.database.base import db
from bot.inlinemode import inline_router, book_router
from bot.middlewares import (
    UserActivityMiddleware,
    IsJoinChannelMiddleware,
    UserSaveMiddleware,
    channel_check_router,
)
from bot.config import conf

load_dotenv()

TOKEN = conf.bot.TOKEN
ADMINS = conf.bot.ADMINS
MAIN_ADMIN = conf.bot.ADMIN

bot = Bot(TOKEN)
dp = Dispatcher()


@dp.startup()
async def on_startup(bot: Bot):
    await db.create_all()

    # Har bir adminga buyruqlar o'rnatish
    for admin_id in ADMINS:
        try:
            await bot.set_my_commands(
                commands=admin_commands,
                scope=BotCommandScopeChat(chat_id=admin_id),
            )
        except Exception as e:
            logging.warning(f"Admin {admin_id} uchun commands o'rnatib bo'lmadi: {e}")

    await bot.set_my_commands(
        commands=user_commands,
        scope=BotCommandScopeAllPrivateChats(),
    )

    # Faqat asosiy adminga start xabari
    try:
        admins_text = "\n".join(f"• <code>{a}</code>" for a in ADMINS)
        await bot.send_message(
            chat_id=MAIN_ADMIN,
            text=(
                "✅ <b>Bot ishga tushdi!</b>\n\n"
                f"👑 Adminlar ({len(ADMINS)} ta):\n{admins_text}"
            ),
            parse_mode="HTML",
        )
    except Exception as e:
        logging.warning(f"Startup xabar yuborib bo'lmadi: {e}")

    logging.info(f"Bot started. Admins: {ADMINS}")


@dp.shutdown()
async def on_shutdown(bot: Bot):
    try:
        await bot.send_message(
            chat_id=MAIN_ADMIN,
            text="❌ Bot to'xtatildi!",
        )
    except Exception:
        pass
    logging.info("Bot stopped")


async def main():
    dp.message.middleware(IsJoinChannelMiddleware())
    dp.message.middleware(UserActivityMiddleware())
    dp.message.middleware(UserSaveMiddleware())

    dp.include_router(channel_check_router)
    dp.include_router(inline_router)
    dp.include_router(book_router)
    dp.include_router(admin_router)
    dp.include_router(user_router)

    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    )
    asyncio.run(main())
