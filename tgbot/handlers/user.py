from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from tgbot.misc.utils import get_info_token

user_router = Router()


@user_router.message(CommandStart())
async def user_start(message: Message):
    await message.reply("Поздравляю, обычный пользователь!")


@user_router.message(F.text)
async def user_get_token(message: Message):
    url = "https://dexscreener.com/solana/7qbrf6ysyguluvs6y1q64bdvrfe4zcuuz1jrdovnujnm"
    await get_info_token(url)
    await message.reply(message.text + " - твой токен")
