from aiogram import BaseMiddleware
from aiogram.types import Message

from bot.database.models.users import User


class UserSaveMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        if not event.from_user:
            return await handler(event, data)

        user = await User.get_with_tg_id(event.from_user.id)
        if user is None:
            await User.create(
                tg_id=event.from_user.id,
                first_name=event.from_user.first_name,
                last_name=event.from_user.last_name,
                username=event.from_user.username,
            )

        return await handler(event, data)
