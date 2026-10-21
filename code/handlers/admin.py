from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from db import is_admin, add_admin, update_money, update_xp
from config import ADMIN_PASSWORD

router = Router()


@router.message(Command("admin"))
async def cmd_admin(message: Message):
    if not await is_admin(message.from_user.id):
        await message.answer("🔐 Введите пароль администратора одной строкой:")
    else:
        await message.answer(
            "🛠 **Админ-панель**\n\n"
            "/give_money <user_id> <amount>\n"
            "/set_xp <user_id> <amount>\n"
            "/make_admin <user_id>",
            parse_mode="Markdown"
        )


@router.message(F.text.regexp(r"^[A-Za-z0-9]{10,}$"))
async def check_password(message: Message):
    if await is_admin(message.from_user.id):
        return
    if message.text == ADMIN_PASSWORD:
        await add_admin(message.from_user.id)
        await message.answer("✅ Доступ получен. Команды: /give_money, /set_xp, /make_admin")
    else:
        await message.answer("❌ Неверный пароль")


@router.message(Command("give_money"))
async def cmd_give_money(message: Message):
    if not await is_admin(message.from_user.id):
        return
    parts = message.text.split()
    if len(parts) != 3:
        await message.answer("Использование: /give_money <user_id> <amount>")
        return
    try:
        uid = int(parts[1])
        amount = int(parts[2])
        await update_money(uid, amount)
        await message.answer(f"✅ Игроку {uid} начислено ${amount}")
    except ValueError:
        await message.answer("Ошибка в числах")


@router.message(Command("set_xp"))
async def cmd_set_xp(message: Message):
    if not await is_admin(message.from_user.id):
        return
    parts = message.text.split()
    if len(parts) != 3:
        await message.answer("Использование: /set_xp <user_id> <amount>")
        return
    try:
        uid = int(parts[1])
        amount = int(parts[2])
        await update_xp(uid, amount)
        await message.answer(f"✅ Игроку {uid} добавлено {amount} XP")
    except ValueError:
        await message.answer("Ошибка в числах")


@router.message(Command("make_admin"))
async def cmd_make_admin(message: Message):
    if not await is_admin(message.from_user.id):
        return
    parts = message.text.split()
    if len(parts) != 2:
        await message.answer("Использование: /make_admin <user_id>")
        return
    try:
        uid = int(parts[1])
        await add_admin(uid)
        await message.answer(f"✅ Игрок {uid} теперь админ")
    except ValueError:
        await message.answer("Ошибка в user_id")
