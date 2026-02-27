from aiogram import Router

from bot.filters.admin_filter import isAdmin
from bot.admin.broadcast import router as broadcast
from bot.admin.channels import router as channels
from bot.admin.help import router as help
from bot.admin.reply import router as reply
from bot.admin.start import router as start
from bot.admin.statistic import statistic_router

admin_router = Router()
admin_router.message.filter(isAdmin())
admin_router.include_router(statistic_router)
admin_router.include_router(broadcast)
admin_router.include_router(channels)
admin_router.include_router(help)
admin_router.include_router(reply)
admin_router.include_router(start)
