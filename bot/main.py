import os
import sys
import logging
import asyncio


from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, BotCommandScopeChat
from dotenv import load_dotenv

from bot.admin import admin_router
from bot.routers import user_router
from bot.database.base import db
from bot.admin.commands import admin_commands
from bot.inlinemode import inline_router
from bot.middlewares import (
    UserActivityMiddleware,
    IsJoinChannelMiddleware,
    UserSaveMiddleware,
)


load_dotenv()

TOKEN = os.getenv("TOKEN")
ADMIN = int(os.getenv("ADMIN"))
bot = Bot(TOKEN)
dp = Dispatcher()


@dp.startup()
async def startup(bot: Bot):
    await db.create_all()
    await bot.set_my_commands(
        commands=admin_commands, scope=BotCommandScopeChat(chat_id=ADMIN)
    )
    await bot.send_message(chat_id=ADMIN, text="Bot started✅")


@dp.shutdown()
async def shutdown(bot: Bot):
    await bot.send_message(chat_id=ADMIN, text="Bot stopped❌")


async def main():
    dp.message.middleware(IsJoinChannelMiddleware())
    dp.message.middleware(UserActivityMiddleware())
    dp.message.middleware(UserSaveMiddleware())
    dp.include_router(admin_router)
    dp.include_router(user_router)
    dp.include_router(inline_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
