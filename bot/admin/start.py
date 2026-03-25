from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import Message, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    ikm = InlineKeyboardBuilder()
    ikm.add(
        InlineKeyboardButton(
            text="🔍 Kitob qidirish",
            switch_inline_query_current_chat="",
        )
    )
    ikm.add(
        InlineKeyboardButton(
            text="➕ Kitob qo'shish",
            callback_data="add_book",  # ✅ inline tugma
        )
    )
    await message.answer("Xush kelibsiz!", reply_markup=ikm.as_markup())


# @router.callback_query(F.data == "add_book")
# async def add_book_callback(callback, state: FSMContext):
#     await state.set_state(AddBook.title)

#     await callback.message.answer(
#         "📚 Kitob nomini kiriting:",
