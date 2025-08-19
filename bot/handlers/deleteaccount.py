from aiogram import types
from aiogram.dispatcher import Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.db.session import SessionLocal
from bot.db.models import User, UserGenLimit
from sqlalchemy.orm import joinedload

pending_account_deletion = set()


async def deleteaccount_handler(message: types.Message):
    user_id = message.from_user.id
    print(f"👉 /deleteaccount вызван пользователем {user_id}")

    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            "✅ Подтвердить удаление", callback_data="confirm_delete_account"
        ),
        InlineKeyboardButton("❌ Отмена", callback_data="cancel_delete_account"),
    )

    pending_account_deletion.add(user_id)

    await message.reply(
        "⚠️ Вы уверены, что хотите <b>удалить аккаунт</b>?\n"
        "Это действие <u>удалит все каналы, лимиты и ваши данные</u> без возможности восстановления.",
        reply_markup=keyboard,
        parse_mode="HTML",
    )


async def deleteaccount_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    action = callback.data

    if user_id not in pending_account_deletion:
        await callback.message.edit_text("❌ Нет активной операции удаления.")
        return

    if action == "cancel_delete_account":
        pending_account_deletion.remove(user_id)
        await callback.message.edit_text("❎ Удаление аккаунта отменено.")
        return

    if action == "confirm_delete_account":
        db = SessionLocal()
        user = (
            db.query(User)
            .options(joinedload(User.channels))
            .filter_by(tg_id=user_id)
            .first()
        )

        if not user:
            await callback.message.edit_text("❌ Пользователь не найден.")
            db.close()
            return

        # Удалим лимиты генераций вручную
        db.query(UserGenLimit).filter_by(user_id=user_id).delete()

        db.delete(user)  # удалит и UserChannel благодаря cascade
        db.commit()
        db.close()

        pending_account_deletion.remove(user_id)
        await callback.message.edit_text("✅ Ваш аккаунт и все данные успешно удалены.")


def register_deleteaccount_handler(dp: Dispatcher):
    dp.register_message_handler(deleteaccount_handler, commands=["deleteaccount"])
    dp.register_callback_query_handler(
        deleteaccount_callback, text_startswith="confirm_delete_account"
    )
    dp.register_callback_query_handler(
        deleteaccount_callback, text_startswith="cancel_delete_account"
    )
