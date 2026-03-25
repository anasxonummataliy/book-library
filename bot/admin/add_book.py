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
from bot.database.base import db

add_router = Router()


class AddBook(StatesGroup):
    title = State()
    author = State()
    language = State()
    description = State()
    cover = State()
    file = State()


LANGUAGES = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🇺🇿 UZ"), KeyboardButton(text="🇷🇺 RU")],
        [KeyboardButton(text="🇬🇧 EN"), KeyboardButton(text="❌ Bekor qilish")],
    ],
    resize_keyboard=True,
)

SKIP = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="⏭ O'tkazib yuborish")]],
    resize_keyboard=True,
)

CANCEL = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="❌ Bekor qilish")]],
    resize_keyboard=True,
)

@add_router.callback_query(F.data == "add_book")
async def start_adding(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddBook.title)
    await callback.message.answer("📚 Kitob nomini kiriting:", reply_markup=CANCEL)


@add_router.message(AddBook.title)
async def get_title(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await cancel(message, state)
        return

    await state.update_data(title=message.text)
    await state.set_state(AddBook.author)
    await message.answer("✍️ Muallifni kiriting:", reply_markup=CANCEL)


@add_router.message(AddBook.author)
async def get_author(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await cancel(message, state)
        return

    await state.update_data(author=message.text)
    await state.set_state(AddBook.language)
    await message.answer("🌐 Tilni tanlang:", reply_markup=LANGUAGES)


@add_router.message(AddBook.language)
async def get_language(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await cancel(message, state)
        return

    lang_map = {
        "🇺🇿 UZ": "uz",
        "🇷🇺 RU": "ru",
        "🇬🇧 EN": "en",
    }
    lang = lang_map.get(message.text)
    if not lang:
        await message.answer("❗ Iltimos, tugmalardan birini tanlang.")
        return

    await state.update_data(language=lang)
    await state.set_state(AddBook.description)
    await message.answer("📝 Tavsif kiriting:", reply_markup=SKIP)


@add_router.message(AddBook.description)
async def get_description(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await cancel(message, state)
        return

    description = None if message.text == "⏭ O'tkazib yuborish" else message.text
    await state.update_data(description=description)
    await state.set_state(AddBook.cover)
    await message.answer("🖼 Muqova rasmini yuboring:", reply_markup=SKIP)


@add_router.message(AddBook.cover)
async def get_cover(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await cancel(message, state)
        return

    cover_image_id = None
    if message.text == "⏭ O'tkazib yuborish":
        pass
    elif message.photo:
        cover_image_id = message.photo[-1].file_id
    else:
        await message.answer("❗ Rasm yuboring yoki o'tkazib yuboring.")
        return

    await state.update_data(cover_image_id=cover_image_id)
    await state.set_state(AddBook.file)
    await message.answer(
        "📄 Kitob faylini yuboring (PDF yoki boshqa format):", reply_markup=CANCEL
    )


@add_router.message(AddBook.file)
async def get_file(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await cancel(message, state)
        return

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

    await Book.save_model(book)  # BookRepository dagi save metodi
    await state.clear()

    await message.answer(
        f"✅ Kitob muvaffaqiyatli qo'shildi!\n\n"
        f"📚 *{book.title}*\n"
        f"✍️ _{book.author}_",
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardRemove(),
    )


async def cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("❌ Bekor qilindi.", reply_markup=ReplyKeyboardRemove())
