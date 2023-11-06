from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from tgbot.misc.utils import get_all_info_token
from tgbot.handlers.admin import admin_send_error

user_router = Router()


@user_router.message(CommandStart())
async def user_start(message: Message):
    await message.reply("Поздравляю, обычный пользователь!")


@user_router.message(F.text)
async def user_get_token(message: Message):
    try:
        results = await get_all_info_token(message.text)
        await message.reply(results, parse_mode="HTML")
    except Exception as e:
        await message.reply(f"не найден токен {message.text} или произошла ошибка")
        await admin_send_error(message, str(e))
