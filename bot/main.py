import os
import sys
import logging
import asyncio


from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message, BotCommandScopeChat

from bot.admin.commands import admin_commands 

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("TOKEN")
ADMIN = int(os.getenv("ADMIN"))
bot = Bot(TOKEN)
dp = Dispatcher()

@dp.startup()
async def startup(bot: Bot):
    await bot.set_my_commands(commands=admin_commands, scope=BotCommandScopeChat(chat_id=ADMIN))
    await bot.send_message(chat_id=ADMIN, text='Bot started✅')

@dp.shutdown()
async def shutdown(bot: Bot):
    await bot.send_message(chat_id=ADMIN, text='Bot stopped❌')

@dp.message(CommandStart)
async def start_handler(msg: Message):
    await msg.answer(f"Salom {msg.from_user.first_name}")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
