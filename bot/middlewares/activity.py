from datetime import datetime

from aiogram import BaseMiddleware
from aiogram.types import Message

from bot.database.session import get_async_session_context
from bot.database.models.users import User
from sqlalchemy import select


class UserActivityMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        if isinstance(event, Message) and event.from_user:
            async with get_async_session_context() as session:
                result = await session.execute(
                    select(User).where(User.tg_id == event.from_user.id)
                )
                user = result.scalar_one_or_none()
                if user:
                    user.last_activity = datetime.now()
                    user.is_blocked = False
                    await session.commit()

        return await handler(event, data)
