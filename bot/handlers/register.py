from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text
from bot.db.session import SessionLocal
from bot.db.models import User, UserChannel


def get_tariff_keyboard():
    return InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("Free", callback_data="tariff_free"),
        InlineKeyboardButton("Basic", callback_data="tariff_pro"),
        InlineKeyboardButton("Pro", callback_data="tariff_pro"),
    )


async def register_autogen(message: types.Message):
    user_id = message.from_user.id
    db = SessionLocal()
    user = db.query(User).filter_by(tg_id=user_id).first()

    if not user:
        user = User(tg_id=user_id, registration_step="awaiting_tariff")
        db.add(user)
        db.commit()
        await message.answer(
            "🚀 Давайте настроим автогенерацию. Выберите тариф:",
            reply_markup=get_tariff_keyboard(),
        )
    elif user.registration_step:
        if user.registration_step == "awaiting_tariff":
            await message.answer(
                "🔁 Вы ещё не выбрали тариф. Выберите тариф:",
                reply_markup=get_tariff_keyboard(),
            )
        elif user.registration_step == "awaiting_channel":
            await message.answer(
                "🔁 Вы уже выбрали тариф. Теперь пришлите @username вашего канала."
            )
    else:
        await message.answer(
            "✅ Вы уже зарегистрированы. Можете использовать /addprompt"
        )
    db.close()


async def tariff_chosen(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    tariff = callback.data.split("_")[1]

    db = SessionLocal()
    user = db.query(User).filter_by(tg_id=user_id).first()
    if not user:
        await callback.answer("❌ Сначала вызовите /register_autogen")
        db.close()
        return

    user.subscription_level = tariff
    user.registration_step = "awaiting_channel"
    db.commit()
    db.close()

    await callback.message.edit_reply_markup()
    await callback.message.answer(
        f"✅ Тариф <b>{tariff}</b> выбран.\nТеперь отправьте @username вашего канала.",
        parse_mode="HTML",
    )


async def channel_received(message: types.Message):
    user_id = message.from_user.id
    db = SessionLocal()
    user = db.query(User).filter_by(tg_if=user_id).first()

    if not user or user.registration_step != "awaiting_channel":
        db.close()
        return

    channel_id = message.text.strip()

    existing = db.query(UserChannel).filter_by(tg_channel_id=channel_id).first()
    if existing:
        await message.answer("⚠️ Этот канал уже зарегистрирован кем-то другим.")
        db.close()
        return

    new_channel = UserChannel(
        user_id=user.id, tg_channel_id=channel_id, title=channel_id, is_active=True
    )
    db.add(new_channel)

    user.registration_step = None  # Registation is done
    db.commit()
    db.close()

    await message.answer(
        f"✅ Канал <b>{channel_id}</b> зарегистрирован!\nТеперь вы можете использовать /addprompt для настройки промта.",
        parse_mode="HTML",
    )


def register_handler(dp: Dispatcher):
    dp.register_message_handler(register_autogen, commands=["register_autogen"])
    dp.register_callback_query_handler(tariff_chosen, Text(startswith="tariff_"))
    dp.register_message_handler(channel_received, content_types=types.ContentType.TEXT)
