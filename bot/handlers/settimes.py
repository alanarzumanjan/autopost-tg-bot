from aiogram import types
from aiogram.dispatcher import Dispatcher
from bot.db.session import SessionLocal
from bot.db.models import User, UserChannel
import re
import json

TARIFF_LIMITS = {"free": 1, "basic": 2, "pro": 5, "unlimited": 10}


def is_valid_time_format(time_str):
    return re.match(r"^\d{2}:\d{2}$", time_str)


async def settimes_handler(message: types.Message):
    user_id = message.from_user.id
    args = message.get_args().strip().split()

    if len(args) < 2:
        await message.reply(
            "❗ Пример:\n<code>/settimes @канал 09:00 13:00 19:00</code>",
            parse_mode="HTML",
        )
        return

    channel_id = args[0]
    time_list = args[1:]

    invalid_times = [t for t in time_list if not is_valid_time_format(t)]
    if invalid_times:
        await message.reply(f"❌ Неверный формат времени: {' '.join(invalid_times)}")
        return

    db = SessionLocal()
    user = db.query(User).filter_by(tg_id=user_id).first()
    if not user:
        await message.reply("❌ Сначала зарегистрируйтесь: /register_autogen")
        db.close()
        return

    limit = TARIFF_LIMITS.get(user.subscription_level, 1)
    if limit is None:  # unlimited
        limit = 100

    if len(time_list) > limit:
        await message.reply(f"⚠️ Ваш тариф позволяет максимум {limit} постов в день.")
        db.close()
        return

    channel = (
        db.query(UserChannel)
        .filter_by(user_id=user.id, tg_channel_id=channel_id)
        .first()
    )
    if not channel:
        await message.reply("❌ Канал не найден или не принадлежит вам.")
        db.close()
        return

    # Сохраняем
    channel.posts_per_day = len(time_list)
    if hasattr(channel, "set_post_times"):
        channel.set_post_times(time_list)  # json-строка
    else:
        channel.post_times = time_list  # ARRAY

    db.commit()
    db.close()

    await message.reply(
        f"✅ Время публикаций для {channel_id} установлено: {', '.join(time_list)}"
    )


def register_settimes_handler(dp: Dispatcher):
    dp.register_message_handler(settimes_handler, commands=["settimes"])
