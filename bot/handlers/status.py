from aiogram import types
from aiogram.dispatcher import Dispatcher
from bot.db.session import SessionLocal
from bot.db.models import User, UserChannel, UserGenLimit
import json

TARIFF_LIMITS = {"free": 1, "basic": 2, "pro": 4, "unlimited": None}


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

    result = f"<b>👤 Ваш профиль</b>\n"
    result += f"🆔 <code>{user.tg_id}</code>\n"
    result += f"💳 Тариф: <b>{user.subscription_level}</b>\n"
    result += f"🧠 Генерации: {gen_info}\n\n"

    if not channels:
        result += "📋 Нет зарегистрированных каналов."
    else:
        result += "<b>📋 Ваши каналы:</b>\n"
        for ch in channels:
            if hasattr(ch, "get_post_times"):
                times = ch.get_post_times()
            else:
                times = ch.post_times or []

            if isinstance(times, str):
                try:
                    times = json.loads(times)
                except:
                    times = []

            times_str = ", ".join(times) if times else "не указано"
            result += (
                f"📢 <b>{ch.title}</b> ({ch.tg_channel_id})\n"
                f"• Постов в день: {ch.posts_per_day or 0}\n"
                f"• Время: {times_str}\n\n"
            )

    await message.answer(result.strip(), parse_mode="HTML")


def register_status_handler(dp: Dispatcher):
    dp.register_message_handler(status_handler, commands=["status"])
