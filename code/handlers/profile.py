from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from db import get_user, is_admin
from config import ADMIN_PASSWORD, WEBAPP_URL
from aiogram.types import WebAppInfo

router = Router()


@router.callback_query(F.data == "profile")
async def show_profile(callback: CallbackQuery):
    user = await get_user(callback.from_user.id)
    if not user:
        await callback.answer("Сначала нажми /start", show_alert=True)
        return

    user_id, username, first_name, money, level, xp, location, transport, *_ = user

    text = (
        f"👤 **{first_name}**\n"
        f"🆔 ID: `{user_id}`\n"
        f"💰 Баланс: **${money}**\n"
        f"⭐ Уровень: **{level}** (XP: {xp})\n"
        f"📍 Локация: `{location}`\n"
        f"🚗 Транспорт: {transport}\n"
    )

    is_adm = await is_admin(callback.from_user.id)

    kb_rows = [
        [InlineKeyboardButton(text="🗺 Карта", web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton(text="💼 Работать (таксист)", callback_data="work_taxi")],
    ]

    if is_adm:
        kb_rows.append([
            InlineKeyboardButton(text=f"🛠 {first_name}", callback_data="admin_panel")
        ])

    kb = InlineKeyboardMarkup(inline_keyboard=kb_rows)
    await callback.message.edit_text(text, reply_markup=kb, parse_mode="Markdown")
    await callback.answer()


@router.callback_query(F.data == "admin_panel")
async def admin_panel(callback: CallbackQuery):
    is_adm = await is_admin(callback.from_user.id)
    if not is_adm:
        await callback.message.answer("🔐 Введите пароль администратора:")
        # простая проверка: ждём следующее сообщение
        # (упрощённо — флаг ставим в FSM; для MVP сделаем прямой ответ)
        await callback.answer()
    else:
        from aiogram.fsm.context import FSMContext
        await callback.message.answer("Ты уже админ. Команды: /give_money, /set_level")
        await callback.answer()
