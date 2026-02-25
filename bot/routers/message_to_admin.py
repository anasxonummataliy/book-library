from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from bot.config import conf

message_to_admin_router = Router()

ADMIN_ID = conf.bot.ADMIN


class MessageToAdminState(StatesGroup):
    mess = State()


@message_to_admin_router.message(Command("admin"))
async def message_to_admin_handler(message: Message, state: FSMContext):
    await state.set_state(MessageToAdminState.mess)
    await message.answer("Adminga yuboriladigan xabaringizni kiriting:")


@message_to_admin_router.message(MessageToAdminState.mess)
async def message_to_admin_handler(message: Message, bot: Bot, state: FSMContext):
    user_id = message.from_user.id
    text = (
        f"📩 <b>Yangi xabar</b>\n"
        f"━━━━━━━━━━━━━━━\n"
        f"👤 User ID: <code>{user_id}</code>\n"
        f"💬 {message.text}"
    )
    await bot.send_message(ADMIN_ID, text, parse_mode="HTML")
    await message.answer("Adminga yuborildi ✅")
