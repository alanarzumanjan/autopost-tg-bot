from aiogram import types
from aiogram.dispatcher import Dispatcher
from bot.db.session import SessionLocal
from bot.db.models import User

VALID_TARIFFS = ["free", "basic", "pro", "unlimited"]


async def settariff_handler(message: types.Message):
    user_id = message.from_user.id
    args = message.get_args().strip().lower()

    if args not in VALID_TARIFFS:
        await message.reply(
            "❗ Укажите тариф из списка:\n"
            "<code>/settariff free</code>\n"
            "<code>/settariff basic</code>\n"
            "<code>/settariff pro</code>\n"
            "<code>/settariff unlimited</code>",
            parse_mode="HTML",
        )
        return

    db = SessionLocal()
    user = db.query(User).filter_by(tg_id=user_id).first()

    if not user:
        await message.reply("❌ Сначала зарегистрируйтесь через /register_autogen.")
        db.close()
        return

    user.subscription_level = args
    db.commit()
    db.close()

    await message.reply(f"✅ Ваш тариф теперь: <b>{args}</b>", parse_mode="HTML")


def register_settariff_handler(dp: Dispatcher):
    dp.register_message_handler(settariff_handler, commands=["settariff"])
