from aiogram import types
from aiogram.dispatcher import Dispatcher


async def templates_handler(message: types.Message):
    await message.answer(
        "<b>🎨 Доступные стили генерации:</b>\n\n"
        "• <b>smart</b> — 📘 Умный и полезный\n"
        "    <i>По умолчанию: нейтральный тон, конкретика и польза</i>\n\n"
        "• <b>bold</b> — 🔥 Дерзкий и уверенный\n"
        "    <i>Смелый стиль, уверенные тезисы, чуть вызова</i>\n\n"
        "• <b>educational</b> — 🎓 Образовательный\n"
        "    <i>Подача как у преподавателя, с примерами и аргументами</i>\n\n"
        "• <b>twitter</b> — 🐦 Кратко и по делу\n"
        "    <i>Каждая мысль — как твит. Жесткая лаконичность</i>\n\n"
        "• <b>story</b> — 📖 Через истории\n"
        "    <i>Начинается с короткой ситуации или кейса, вывод в конце</i>\n\n"
        "👉 Установить стиль: <code>/settemplate @канал стиль</code>",
        parse_mode="HTML",
    )


def register_templates_handler(dp: Dispatcher):
    dp.register_message_handler(templates_handler, commands=["templates"])
