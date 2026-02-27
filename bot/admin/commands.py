from aiogram.types import BotCommand

admin_commands = [
    BotCommand(command="/start", description="Boshlash 🏁"),
    BotCommand(command="/statistic", description="Foydalanuvchilar haqida ma'lumot💽"),
    BotCommand(command="/channels", description="Kanallar ro‘yxati 📢"),
    BotCommand(command="/add_channel", description="Majburiy kanal qo‘shish ➕"),
    BotCommand(
        command="/broadcast", description="Barcha foydalanuvchilarga xabar yuborish 📣"
    ),
    BotCommand(command="/reply", description="Biror foydalanuvchiga javob qaytarish ✉️"),
    BotCommand(command="/help", description="Yordam ❓"),
]
