from aiogram import Router, Bot
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.keyboard import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)

from bot.config import conf

message_to_admin_router = Router()


class MessageToAdminState(StatesGroup):
    waiting = State()


CANCEL_KB = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="❌ Bekor qilish")]],
    resize_keyboard=True,
)


@message_to_admin_router.message(Command("contact"))
async def contact_handler(message: Message, state: FSMContext):
    await state.set_state(MessageToAdminState.waiting)
    await message.answer(
        "✉️ <b>Adminga xabar yuborish</b>\n\n" "Xabaringizni kiriting:",
        parse_mode="HTML",
        reply_markup=CANCEL_KB,
    )


@message_to_admin_router.message(MessageToAdminState.waiting)
async def send_to_admin(message: Message, bot: Bot, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Bekor qilindi.", reply_markup=ReplyKeyboardRemove())
        return

    user = message.from_user
    username = f"@{user.username}" if user.username else "yo'q"
    text = (
        f"📩 <b>Yangi xabar keldi</b>\n"
        f"━━━━━━━━━━━━━━━\n"
        f"👤 Ismi: <b>{user.full_name}</b>\n"
        f"🆔 ID: <code>{user.id}</code>\n"
        f"📎 Username: {username}\n"
        f"━━━━━━━━━━━━━━━\n"
        f"💬 {message.text}"
    )

    # Xabar barcha adminlarga yuboriladi
    sent = 0
    for admin_id in conf.bot.ADMINS:
        try:
            await bot.send_message(admin_id, text, parse_mode="HTML")
            sent += 1
        except Exception:
            pass

    if sent:
        await message.answer(
            "✅ Xabaringiz adminga yuborildi!", reply_markup=ReplyKeyboardRemove()
        )
    else:
        await message.answer(
            "❌ Xabar yuborishda xatolik yuz berdi.", reply_markup=ReplyKeyboardRemove()
        )

    await state.clear()
