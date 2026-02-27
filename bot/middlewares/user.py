from aiogram import BaseMiddleware
from aiogram.types import Message

from bot.database.models.users import User
from bot.database.session import get_async_session_context


class UserSaveMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data):
        users = await User.get_all()
        user_id = event.from_user.id

        if user_id not in [user.tg_id for user in users]:
            await User.create(
                tg_id=user_id,
                first_name=event.from_user.first_name,
                last_name=event.from_user.last_name,
                username=event.from_user.username,
            )
        return await handler(event, data)
