from aiogram import types
from aiogram.dispatcher import Dispatcher
from bot.db.session import SessionLocal
from bot.db.models import User, UserChannel


async def addprompt_handler(message: types.Message):
    user_id = message.from_user.id
    args = message.get_args().strip()

    if not args or "@" not in args or " " not in args:
        await message.reply(
            "❗ Как использовать:\n"
            "<code>/addprompt @канал текст_промта</code>\n\n"
            "Пример:\n"
            "<code>/addprompt @mychannel Пиши посты про бизнес и Telegram</code>",
            parse_mode="HTML",
        )
        return

    try:
        channel_id, prompt_text = args.split(" ", 1)
        channel_id = channel_id.strip()
        prompt_text = prompt_text.strip()
    except Exception:
        await message.reply(
            "⚠️ Неверный формат. Убедитесь, что указали канал и текст промта."
        )
        return

    db = SessionLocal()
    user = db.query(User).filter_by(tg_id=user_id).first()

    if not user:
        await message.reply("❌ Сначала зарегистрируйтесь через /register_autogen.")
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

    await message.reply(
        f"✅ Промт для <b>{channel_id}</b> сохранён!\n\n"
        f"Теперь при генерации будут использоваться ваши инструкции.",
        parse_mode="HTML",
    )


def register_addprompt_handler(dp: Dispatcher):
    dp.register_message_handler(addprompt_handler, commands=["addprompt", "addpromt"])
