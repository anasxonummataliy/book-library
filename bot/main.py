import os
import sys
import logging
import asyncio


from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("TOKEN")
ADMIN = int(os.getenv("ADMIN"))
bot = Bot(TOKEN)
dp = Dispatcher()

@dp.startup()
async def startup(bot: Bot):
    await bot.send_message(chat_id=ADMIN, text='Bot started✅')

@dp.shutdown()
async def shutdown(bot: Bot):
    await bot.send_message(chat_id=ADMIN, text='Bot stopped❌')

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())