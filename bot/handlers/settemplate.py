from aiogram import types
from aiogram.dispatcher import Dispatcher
from bot.db.session import SessionLocal
from bot.db.models import User, UserChannel

VALID_TEMPLATES = {
    "smart": "📘 Умный и полезный",
    "bold": "🔥 Дерзкий и уверенный",
    "educational": "🎓 Образовательный",
    "twitter": "🐦 Кратко и по делу",
    "story": "📖 Через истории",
}


async def settemplate_handler(message: types.Message):
    args = message.get_args().strip().split()
    user_id = message.from_user.id

    if len(args) != 2:
        await message.reply(
            "❗ Использование:\n<code>/settemplate @канал стиль</code>\n\n"
            "Доступные стили:\n"
            + "\n".join([f"{k} — {v}" for k, v in VALID_TEMPLATES.items()]),
            parse_mode="HTML",
        )
        return

    channel_id, template = args[0], args[1].lower()

    if template not in VALID_TEMPLATES:
        await message.reply(
            "⚠️ Неверный стиль. Допустимые:\n" + ", ".join(VALID_TEMPLATES.keys())
        )
        return

    db = SessionLocal()
    user = db.query(User).filter_by(tg_id=user_id).first()
    if not user:
        await message.reply("❌ Вы не зарегистрированы.")
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

    channel.template = template
    db.commit()
    db.close()

    await message.reply(
        f"✅ Стиль генерации для {channel_id} установлен: <b>{VALID_TEMPLATES[template]}</b>",
        parse_mode="HTML",
    )


def register_settemplate_handler(dp: Dispatcher):
    dp.register_message_handler(settemplate_handler, commands=["settemplate"])
