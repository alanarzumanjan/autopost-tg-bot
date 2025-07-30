from aiogram import types
from aiogram.dispatcher import Dispatcher
from bot.db.session import SessionLocal
from bot.db.models import User, UserChannel


async def deletechannel_handler(message: types.Message):
    user_id = message.from_user.id
    args = message.get_args().strip()

    if not args or not args.startswith("@"):
        await message.reply(
            "❗ Укажите канал: <code>/deletechannel @channel</code>", parse_mode="HTML"
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

    db.delete(channel)
    db.commit()
    db.close()

    await message.reply(f"✅ Канал {tg_channel_id} успешно удалён.")


def register_deletechannel_handler(dp: Dispatcher):
    dp.register_message_handler(deletechannel_handler, commands=["deletechannel"])
