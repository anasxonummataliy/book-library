from aiogram import Router

from .basic import main_router

user_router = Router()
user_router.include_router(main_router)
