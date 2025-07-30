from aiogram import types
from aiogram.dispatcher import Dispatcher
from bot.db.session import SessionLocal
from bot.db.models import User, UserChannel


async def addprompt_handler(message: types.Message):
    user_id = message.from_user.id
    args = message.get_args().strip()

    if not args or "@" not in args:
        await message.reply(
            "❗ Использование:\n<code>/addprompt @channel ваш промт</code>",
            parse_mode="HTML",
        )
        return

    try:
        parts = args.split(" ", 1)
        channel_id = parts[0].strip()
        prompt_text = parts[1].strip()
    except Exception:
        await message.reply("⚠️ Неверный формат команды. Укажите канал и промт.")
        return

    db = SessionLocal()
    user = db.query(User).filter_by(tg_id=user_id).first()

    if not user:
        await message.reply("❌ Сначала пройдите регистрацию: /register_autogen")
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

    channel.custom_prompt = prompt_text
    db.commit()
    db.close()

    await message.reply(f"✅ Промт для канала {channel_id} сохранён.")


def register_addprompt_handler(dp: Dispatcher):
    dp.register_message_handler(addprompt_handler, commands=["addprompt"])
