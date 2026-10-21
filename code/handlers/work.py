import random
from aiogram import Router, F
from aiogram.types import CallbackQuery
from db import get_user, update_money, update_xp

router = Router()


@router.callback_query(F.data == "work_taxi")
async def work_taxi(callback: CallbackQuery):
    user = await get_user(callback.from_user.id)
    if not user:
        await callback.answer("Сначала /start", show_alert=True)
        return

    earnings = random.randint(50, 150)
    xp_gain = random.randint(5, 15)

    await update_money(callback.from_user.id, earnings)
    await update_xp(callback.from_user.id, xp_gain)

    user = await get_user(callback.from_user.id)
    money = user[3]

    await callback.message.answer(
        f"🚕 Поработал таксистом!\n"
        f"💵 Заработал: **${earnings}**\n"
        f"⭐ XP: +{xp_gain}\n"
        f"💰 Баланс: **${money}**",
        parse_mode="Markdown"
    )
    await callback.answer()                
