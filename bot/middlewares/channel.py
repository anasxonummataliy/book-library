from sqlalchemy import select

from aiogram import BaseMiddleware, Bot, Router, F
from aiogram.enums import ChatType, ChatMemberStatus
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery

from bot.database.models.channels import Channel
from bot.database.session import get_async_session_context


async def get_channel_ids() -> list[int]:
    async with get_async_session_context() as session:
        result = await session.execute(select(Channel.tg_id))
        return [row[0] for row in result.all()]


router = Router()


class IsJoinChannelMiddleware(BaseMiddleware):

    async def make_channel_buttons(self, bot: Bot, channel_ids: list[int]):
        ikb = InlineKeyboardBuilder()
        for channel_id in channel_ids:
            try:
                channel = await bot.get_chat(chat_id=channel_id)
                url = channel.invite_link or (
                    f"https://t.me/{channel.username}" if channel.username else None
                )
                if url:
                    ikb.row(InlineKeyboardButton(text=f"📢 {channel.title}", url=url))
            except Exception as e:
                print(f"Kanal ma'lumotini olishda xatolik {channel_id}: {e}")
        ikb.row(InlineKeyboardButton(text="✅ Tekshirish", callback_data="joined"))
        return ikb.as_markup()

    async def check_subscriptions(self, bot: Bot, user_id: int) -> list[int]:
        unsubscribed = []
        channel_ids = await get_channel_ids()
        for channel_id in channel_ids:
            try:
                member = await bot.get_chat_member(chat_id=channel_id, user_id=user_id)
                if member.status not in (
                    ChatMemberStatus.MEMBER,
                    ChatMemberStatus.CREATOR,
                    ChatMemberStatus.ADMINISTRATOR,
                ):
                    unsubscribed.append(channel_id)
            except Exception:
                unsubscribed.append(channel_id)
        return unsubscribed

    async def __call__(self, handler, event: Message, data: dict):
        if not isinstance(event, Message):
            return await handler(event, data)

        if event.chat.type != ChatType.PRIVATE:
            return

        bot: Bot = data["bot"]
        user_id = event.from_user.id
        unsubscribed = await self.check_subscriptions(bot, user_id)

        if unsubscribed:
            await event.answer(
                "❗️ Botdan foydalanish uchun quyidagi kanallarga obuna bo'ling:",
                reply_markup=await self.make_channel_buttons(bot, unsubscribed),
            )
            return

        return await handler(event, data)


@router.callback_query(F.data == "joined")
async def check_subscription_callback(callback: CallbackQuery, bot: Bot):
    middleware = IsJoinChannelMiddleware()
    unsubscribed = await middleware.check_subscriptions(bot, callback.from_user.id)

    if unsubscribed:
        await callback.answer(
            "❌ Siz hali barcha kanallarga obuna bo'lmadingiz!",
            show_alert=True,
        )
    else:
        await callback.message.delete()
        await callback.message.answer(
            "✅ Tabriklaymiz! Siz barcha kanallarga obuna bo'ldingiz.\n"
            "Endi botdan foydalanishingiz mumkin! 📚"
        )
        await callback.answer()
