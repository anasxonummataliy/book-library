from aiogram import Router, F, Bot
from aiogram.types import Message


router = Router()


@router.message(F.reply_to_message)
async def reply_handler(message: Message, bot: Bot):
    replied_text = message.reply_to_message.text
    print(replied_text)
    import re

    match: re.Match = re.search(r"User ID:\s*(\d+)", replied_text)

    if not match:
        await message.answer("User topilmadi ❌")
        return

    user_id = int(match.group(1))
    await bot.send_message(user_id, f"📩 Admin javobi:\n\n{message.text}")
    await message.answer("Yuborildi ✅")
