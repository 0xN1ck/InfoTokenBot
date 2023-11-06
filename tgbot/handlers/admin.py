from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message

from tgbot.filters.admin import AdminFilter

from tgbot.services import broadcaster
from tgbot.config import load_config
config = load_config(".env")

admin_router = Router()
admin_router.message.filter(AdminFilter())


@admin_router.message(CommandStart())
async def admin_start(message: Message):
    await message.reply("Поздравляю, админ!")


@admin_router.message(F.text)
async def admin_send_error(message: Message, error):
    await broadcaster.broadcast(message.bot, config.tg_bot.admin_ids, error + '\n' + message.text)
