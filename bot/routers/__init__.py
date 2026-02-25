from aiogram import Router

from bot.filters import isAdmin

from .basic import main_router
from .message_to_admin import message_to_admin_router

user_router = Router()
user_router.message.filter(~isAdmin())
user_router.include_routers(main_router, message_to_admin_router)
