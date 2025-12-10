import os
import sys
import logging
import asyncio


from aiogram import Bot, Dispatcher
from aiogram.types import Message

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("TOKEN")
bot = Bot(TOKEN)
dp = Dispatcher()


async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())