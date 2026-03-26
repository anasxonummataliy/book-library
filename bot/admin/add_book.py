from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    CallbackQuery,
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)

from bot.database.models import Book

add_router = Router()


class AddBook(StatesGroup):
    title = State()
    author = State()
    language = State()
    description = State()
    cover = State()
    file = State()


LANGUAGES_KB = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🇺🇿 UZ"), KeyboardButton(text="🇷🇺 RU")],
        [KeyboardButton(text="🇬🇧 EN"), KeyboardButton(text="❌ Bekor qilish")],
    ],
    resize_keyboard=True,
)

SKIP_KB = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="⏭ O'tkazib yuborish")],
        [KeyboardButton(text="❌ Bekor qilish")],
    ],
    resize_keyboard=True,
)

CANCEL_KB = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="❌ Bekor qilish")]],
    resize_keyboard=True,
)

LANG_MAP = {
    "🇺🇿 UZ": "uz",
    "🇷🇺 RU": "ru",
    "🇬🇧 EN": "en",
}


async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Bekor qilindi.", reply_markup=ReplyKeyboardRemove())


@add_router.callback_query(F.data == "add_book")
async def start_adding(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddBook.title)
    await callback.message.answer(
        "📚 <b>Kitob qo'shish</b>\n\nKitob nomini kiriting:",
        parse_mode="HTML",
        reply_markup=CANCEL_KB,
    )
    await callback.answer()


@add_router.message(AddBook.title)
async def get_title(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        return await cancel(message, state)
    await state.update_data(title=message.text)
    await state.set_state(AddBook.author)
    await message.answer("✍️ Muallif ismini kiriting:", reply_markup=CANCEL_KB)


@add_router.message(AddBook.author)
async def get_author(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        return await cancel(message, state)
    await state.update_data(author=message.text)
    await state.set_state(AddBook.language)
    await message.answer("🌐 Kitob tilini tanlang:", reply_markup=LANGUAGES_KB)


@add_router.message(AddBook.language)
async def get_language(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        return await cancel(message, state)
    lang = LANG_MAP.get(message.text)
    if not lang:
        await message.answer("❗ Iltimos, tugmalardan birini tanlang.")
        return
    await state.update_data(language=lang)
    await state.set_state(AddBook.description)
    await message.answer(
        "📝 Tavsif kiriting (yoki o'tkazib yuboring):", reply_markup=SKIP_KB
    )


@add_router.message(AddBook.description)
async def get_description(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        return await cancel(message, state)
    description = None if message.text == "⏭ O'tkazib yuborish" else message.text
    await state.update_data(description=description)
    await state.set_state(AddBook.cover)
    await message.answer(
        "🖼 Muqova rasmini yuboring (yoki o'tkazib yuboring):",
        reply_markup=SKIP_KB,
    )


@add_router.message(AddBook.cover)
async def get_cover(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        return await cancel(message, state)

    cover_id = None
    if message.text == "⏭ O'tkazib yuborish":
        pass
    elif message.photo:
        cover_id = message.photo[-1].file_id
    else:
        await message.answer("❗ Rasm yuboring yoki o'tkazib yuboring.")
        return

    await state.update_data(cover_image_id=cover_id)
    await state.set_state(AddBook.file)
    await message.answer(
        "📄 Kitob faylini yuboring (PDF yoki boshqa format):",
        reply_markup=CANCEL_KB,
    )


@add_router.message(AddBook.file)
async def get_file(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        return await cancel(message, state)

    if not message.document:
        await message.answer("❗ Fayl yuboring.")
        return

    doc = message.document
    data = await state.get_data()

    book = Book(
        title=data["title"],
        author=data["author"],
        language=data["language"],
        description=data.get("description"),
        cover_image_id=data.get("cover_image_id"),
        file_id=doc.file_id,
        file_size=doc.file_size,
    )
    await book.save_model()
    await state.clear()

    cover_status = "✅ Bor" if data.get("cover_image_id") else "❌ Yo'q"
    await message.answer(
        f"✅ <b>Kitob muvaffaqiyatli qo'shildi!</b>\n\n"
        f"📚 Nomi: <b>{book.title}</b>\n"
        f"✍️ Muallif: <i>{book.author}</i>\n"
        f"🌐 Til: <b>{book.language.upper()}</b>\n"
        f"🖼 Muqova: {cover_status}\n"
        f"📦 Hajmi: <b>{book.file_size_mb}</b>",
        parse_mode="HTML",
        reply_markup=ReplyKeyboardRemove(),
    )
