from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from db import create_user, get_user
from config import WEBAPP_URL
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    user = await get_user(message.from_user.id)
    if not user:
        await create_user(
            message.from_user.id,
            message.from_user.username or "",
            message.from_user.first_name or "Игрок"
        )
        text = (
            "👋 Добро пожаловать в **Oneleap RP**!\n\n"
            "Ты зарегистрирован. Тебе выдан стартовый капитал: **$1 000**.\n\n"
            "Открой карту штата:"
        )
    else:
        text = "С возвращением в **Oneleap RP**! 👋\n\nОткрой карту:"

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🗺 Открыть карту", web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton(text="👤 Профиль", callback_data="profile")],
    ])
    await message.answer(text, reply_markup=kb)
