from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.db.session import SessionLocal
from bot.db.models import User, UserChannel

# 👇 временное хранилище: user_id → channel
pending_deletions = {}


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

    pending_deletions[user_id] = tg_channel_id
    db.close()

    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            "✅ Подтвердить удаление", callback_data="confirm_delete_channel"
        ),
        InlineKeyboardButton("❌ Отмена", callback_data="cancel_delete_channel"),
    )

    await message.reply(
        f"⚠️ Вы действительно хотите удалить канал <b>{tg_channel_id}</b>?\nЭто действие необратимо.",
        reply_markup=keyboard,
        parse_mode="HTML",
    )


async def deletechannel_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    action = callback.data

    if action == "cancel_delete_channel":
        await callback.message.edit_text("❎ Удаление отменено.")
        pending_deletions.pop(user_id, None)
        return

    if action == "confirm_delete_channel":
        tg_channel_id = pending_deletions.get(user_id)
        if not tg_channel_id:
            await callback.message.edit_text("❌ Ошибка: нет канала для удаления.")
            return

        db = SessionLocal()
        user = db.query(User).filter_by(tg_id=user_id).first()
        channel = (
            db.query(UserChannel)
            .filter_by(user_id=user.id, tg_channel_id=tg_channel_id)
            .first()
        )

        if not channel:
            await callback.message.edit_text("❌ Канал не найден.")
            db.close()
            return

        db.delete(channel)  # автоматически удалит PostSend благодаря cascade
        db.commit()
        db.close()

        pending_deletions.pop(user_id, None)
        await callback.message.edit_text(
            f"✅ Канал <b>{tg_channel_id}</b> и связанные публикации удалены.",
            parse_mode="HTML",
        )


def register_deletechannel_handler(dp: Dispatcher):
    dp.register_message_handler(deletechannel_handler, commands=["deletechannel"])
    dp.register_callback_query_handler(
        deletechannel_callback, text_startswith="confirm_delete_channel"
    )
    dp.register_callback_query_handler(
        deletechannel_callback, text_startswith="cancel_delete_channel"
    )
