from aiogram import types
from aiogram.dispatcher import Dispatcher
from bot.db.session import SessionLocal
from bot.db.models import User, UserChannel, UserGenLimit

# Для простоты ограничение по тарифу захардкожим:
TARIFF_LIMITS = {
    "free": 5,
    "basic": 10,
    "pro": 20,
}


async def status_handler(message: types.Message):
    user_id = message.from_user.id
    db = SessionLocal()

    user = db.query(User).filter_by(tg_id=user_id).first()

    if not user:
        await message.reply("❌ Вы ещё не зарегистрированы. Введите /register_autogen.")
        db.close()
        return

    channels = db.query(UserChannel).filter_by(user_id=user.id).all()
    limit_row = db.query(UserGenLimit).filter_by(user_id=user_id).first()
    db.close()

    used = limit_row.count if limit_row else 0
    max_allowed = TARIFF_LIMITS.get(user.subscription_level, 5)

    if max_allowed is None:
        gen_info = "♾️ Без ограничений"
    else:
        gen_info = f"{used} / {max_allowed}"

    channel_list = (
        "\n".join([f"• <b>{c.title}</b> ({c.tg_channel_id})" for c in channels])
        or "— нет зарегистрированных каналов"
    )

    await message.answer(
        f"<b>👤 Ваш профиль</b>\n"
        f"🆔 <code>{user.tg_id}</code>\n"
        f"💳 Тариф: <b>{user.subscription_level}</b>\n"
        f"🧠 Генерации: {gen_info}\n\n"
        f"<b>📋 Ваши каналы:</b>\n{channel_list}",
        parse_mode="HTML",
    )


def register_status_handler(dp: Dispatcher):
    dp.register_message_handler(status_handler, commands=["status"])
