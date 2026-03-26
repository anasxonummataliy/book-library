import asyncio

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import (
    ReplyKeyboardMarkup,
    KeyboardButton,
)

from bot.database.models import User
from bot.config import conf

router = Router()


class Broadcast(StatesGroup):
    waiting = State()


CANCEL_KB = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="❌ Bekor qilish")]],
    resize_keyboard=True,
)


@router.message(Command("broadcast"))
async def broadcast_start(message: Message, state: FSMContext):
    users = await User.get_all()
    # Barcha adminlarni chiqarib hisoblash
    count = len([u for u in users if u.tg_id not in conf.bot.ADMINS])
    await state.set_state(Broadcast.waiting)
    await message.answer(
        f"📣 <b>Ommaviy xabar yuborish</b>\n\n"
        f"👥 Foydalanuvchilar soni: <b>{count}</b>\n\n"
        "Yubormoqchi bo'lgan xabaringizni kiriting:",
        parse_mode="HTML",
        reply_markup=CANCEL_KB,
    )


@router.message(Broadcast.waiting)
async def broadcast_send(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Bekor qilindi.", reply_markup=ReplyKeyboardRemove())
        return

    users = await User.get_all()
    success, failed = 0, 0
    status_msg = await message.answer(
        "⏳ Xabar yuborilmoqda...", reply_markup=ReplyKeyboardRemove()
    )

    for user in users:
        if user.tg_id in conf.bot.ADMINS:
            continue
        try:
            await message.bot.copy_message(
                chat_id=user.tg_id,
                from_chat_id=message.chat.id,
                message_id=message.message_id,
            )
            success += 1
        except Exception:
            failed += 1
        await asyncio.sleep(0.05)

    await status_msg.edit_text(
        f"✅ <b>Xabar yuborish yakunlandi!</b>\n\n"
        f"✔️ Muvaffaqiyatli: <b>{success}</b>\n"
        f"❌ Xatolik: <b>{failed}</b>",
        parse_mode="HTML",
    )
    await state.clear()
