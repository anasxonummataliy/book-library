import os
from aiogram.types import Message
from aiogram.filters import Filter

from dotenv import load_dotenv
load_dotenv()


class isAdmin(Filter):
    async def __call__(self, msg: Message):
        return msg.from_user.id == int(os.getenv("ADMIN"))
