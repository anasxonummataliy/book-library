import os

from aiogram import BaseMiddleware, Bot, Router, F
from aiogram.types import Message
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.enums import ChatType, ChatMemberStatus

from dotenv import load_dotenv

load_dotenv()
CHANNELS = os.getenv("CHANNELS").split(',')

router = Router()

class IsJoinChannelsMiddleware(BaseMiddleware):
    async def make_channel_buttons(self):
        pass