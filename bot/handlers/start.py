from aiogram import types
from aiogram.dispatcher import Dispatcher


async def start_handler(message: types.Message):
    await message.answer(
        "<b>👋 Привет! Я — Content Manager Bot</b>\n\n"
        "Я помогаю автоматически генерировать и публиковать посты в ваши Telegram-каналы на основе ИИ.\n\n"
        "<b>📋 Доступные команды:</b>\n"
        "• /register_autogen — зарегистрировать канал для автогенерации\n"
        "• /settariff — выбрать тариф и оплатить\n"
        "• /settimes — указать время постинга\n"
        "• /settemplate — выбрать стиль генерации\n"
        "• /addprompt — задать кастомный промт\n"
        "• /gen — сгенерировать пост вручную\n"
        "• /status — посмотреть ваш тариф, каналы и расписание\n"
        "• /pausechannel /resumechannel — приостановить / возобновить канал\n"
        "• /deletechannel — удалить канал\n"
        "• /deleteaccount — удалить всю учётку\n"
        "• /templates — стили генерации\n"
        "• /previewtemplate — посмотреть пример стиля\n\n"
        "📩 Для связи с админом: /contact_with_admin",
        parse_mode="HTML",
    )


def register_start_handler(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=["start"])
