from aiogram import types
from aiogram.dispatcher import Dispatcher
from bot.generator.generator import generate_post

VALID_TEMPLATES = ["smart", "bold", "educational", "twitter", "story"]


async def previewtemplate_handler(message: types.Message):
    args = message.get_args().strip().lower()

    if not args or args not in VALID_TEMPLATES:
        await message.reply(
            "❗ Пример использования:\n<code>/previewtemplate стиль</code>\n\n"
            "Доступные стили: " + ", ".join(VALID_TEMPLATES),
            parse_mode="HTML",
        )
        return

    await message.reply(
        f"⏳ Генерирую пример стиля <b>{args}</b>...", parse_mode="HTML"
    )

    post = await generate_post(template=args)

    if post:
        await message.answer(post, parse_mode="HTML")
    else:
        await message.answer("❌ Не удалось сгенерировать пример.")


def register_previewtemplate_handler(dp: Dispatcher):
    dp.register_message_handler(previewtemplate_handler, commands=["previewtemplate"])
