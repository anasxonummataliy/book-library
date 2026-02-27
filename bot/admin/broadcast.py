import asyncio
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from bot.database.models import User
from bot.config import conf

router = Router()


class Broadcast(StatesGroup):
    waiting_for_message = State()


@router.message(Command("broadcast"))
async def broadcast_handler(message: Message, state: FSMContext):
    await message.answer("Iltimos, yubormoqchi bo'lgan xabaringizni kiriting:")
    await state.set_state(Broadcast.waiting_for_message)


@router.message(Broadcast.waiting_for_message)
async def broadcast_handler(message: Message, state: FSMContext):
    users = await User.get_all()
    for user in users:
        try:
            if user.tg_id != int(conf.bot.ADMIN):
                await message.bot.send_message(user.tg_id, message.text)
            await asyncio.sleep(0.1)
        except Exception as e:
            print(f"Xatolik yuz berdi: {e}")
    await state.clear()
    await message.answer("Xabar barcha foydalanuvchilarga yuborildi!")
