from aiogram.types import Message
from aiogram.filters import Filter

from bot.config import conf


class isAdmin(Filter):
    async def __call__(self, msg: Message) -> bool:
        return msg.from_user.id in conf.bot.ADMINS
