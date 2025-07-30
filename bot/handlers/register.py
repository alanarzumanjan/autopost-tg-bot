from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.dispatcher.filters import Text
from bot.db.session import SessionLocal
from bot.db.models import User, UserChannel
from aiogram import Bot
from functools import partial


def get_tariff_keyboard():
    return InlineKeyboardMarkup(row_width=2).add(
        InlineKeyboardButton("Free", callback_data="tariff_free"),
        InlineKeyboardButton("Basic", callback_data="tariff_basic"),
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


async def channel_received(message: types.Message, bot: Bot):
    user_id = message.from_user.id
    db = SessionLocal()
    user = db.query(User).filter_by(tg_id=user_id).first()

    if not user or user.registration_step != "awaiting_channel":
        db.close()
        return

    channel_id_raw = message.text.strip()

    # 🛡️ Проверка: существует ли такой канал, получаем его title
    try:
        chat = await bot.get_chat(channel_id_raw)
        channel_title = chat.title
        tg_channel_id = channel_id_raw
    except Exception as e:
        await message.answer(
            f"❌ Не удалось получить канал. Убедитесь, что:\n"
            f"1. Бот добавлен в канал как администратор\n"
            f"2. Вы указали корректный @username или chat_id\n\nОшибка: {e}"
        )
        db.close()
        return

    # 🔍 Проверка: канал уже зарегистрирован этим пользователем?
    existing = (
        db.query(UserChannel)
        .filter_by(tg_channel_id=tg_channel_id, user_id=user.id)
        .first()
    )

    if existing:
        await message.answer("⚠️ Этот канал уже зарегистрирован вами ранее.")
        db.close()
        return

    # ✅ Создаём канал
    new_channel = UserChannel(
        user_id=user.id,
        tg_channel_id=tg_channel_id,
        title=channel_title,
        is_active=True,
    )
    db.add(new_channel)

    user.registration_step = None
    db.commit()
    db.close()

    await message.answer(
        f"✅ Канал <b>{channel_title}</b> (@{tg_channel_id}) зарегистрирован!\n"
        f"Теперь вы можете использовать /addprompt для настройки промта.",
        parse_mode="HTML",
    )


def register_handler(dp: Dispatcher, bot: Bot):
    dp.register_message_handler(register_autogen, commands=["register_autogen"])
    dp.register_callback_query_handler(tariff_chosen, Text(startswith="tariff_"))
    dp.register_message_handler(
        partial(channel_received, bot=bot), content_types=types.ContentType.TEXT
    )
