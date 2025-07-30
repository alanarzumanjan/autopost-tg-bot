from aiogram import types
from aiogram.dispatcher import Dispatcher
from bot.db.session import SessionLocal
from bot.db.models import User, UserChannel


async def pausechannel_handler(message: types.Message):
    await toggle_channel_status(message, active=False)


async def resumechannel_handler(message: types.Message):
    await toggle_channel_status(message, active=True)


async def toggle_channel_status(message: types.Message, active: bool):
    user_id = message.from_user.id
    args = message.get_args().strip()

    if not args or not args.startswith("@"):
        await message.reply(
            "❗ Пример:\n<code>/pausechannel @channel</code>", parse_mode="HTML"
        )
        return

    tg_channel_id = args
    db = SessionLocal()

    user = db.query(User).filter_by(tg_id=user_id).first()
    if not user:
        await message.reply("❌ Вы не зарегистрированы.")
        db.close()
        return

    channel = (
        db.query(UserChannel)
        .filter_by(user_id=user.id, tg_channel_id=tg_channel_id)
        .first()
    )

    if not channel:
        await message.reply("❌ Канал не найден или не принадлежит вам.")
        db.close()
        return

    if channel.is_active == active:
        await message.reply(
            "ℹ️ Этот канал уже " + ("активен." if active else "на паузе.")
        )
        db.close()
        return

    channel.is_active = active
    db.commit()
    db.close()

    await message.reply(
        f"{'✅ Канал активирован' if active else '⏸ Канал приостановлен'}: <b>{tg_channel_id}</b>",
        parse_mode="HTML",
    )


def register_pause_resume_handlers(dp: Dispatcher):
    dp.register_message_handler(pausechannel_handler, commands=["pausechannel"])
    dp.register_message_handler(resumechannel_handler, commands=["resumechannel"])
