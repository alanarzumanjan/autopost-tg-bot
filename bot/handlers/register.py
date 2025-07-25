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
