from aiogram import types
from aiogram.dispatcher import Dispatcher
from bot.generator.generator import generate_post


async def gen_handler(message: type.Message):
    text = message.get_args()

    custom_promt = text.strip() if text else None

    await message.reply("⏳ Генерирую пост...")

    post = await generate_post(custom_prompt=custom_promt)

    if post:
        await message.answer(post, parse_mode="HTML")
    else:
        await message.answer("❌ Не удалось сгенерировать пост.")


def register_gen_handler(dp: Dispatcher):
    dp.register_message_handler(gen_handler, commands=["gen"])
