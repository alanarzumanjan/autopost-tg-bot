from aiogram import types
from aiogram.dispatcher import Dispatcher
from bot.generator.generator import generate_post

user_gen_counter = {}

max_gen_per_user = 5


async def gen_handler(message: types.Message):
    await message.answer("""
        Example: /gen Write post about Women Style
    """)
    user_id = message.from_user.id
    text = message.get_args().strip()

    count = user_gen_counter.get(user_id, 0)

    if count >= max_gen_per_user:
        await message.reply("🚫 Вы достигли лимита генераций (5). Попробуйте позже.")
        return

    custom_promt = text.strip() if text else None
    await message.reply("⏳ Генерирую пост...")

    post = await generate_post(custom_prompt=custom_promt)

    if post:
        await message.answer(post, parse_mode="HTML")
        user_gen_counter[user_id] += 1
    else:
        await message.answer("❌ Не удалось сгенерировать пост.")


def register_gen_handler(dp: Dispatcher):
    dp.register_message_handler(gen_handler, commands=["gen"])


def reset_generation_limits():
    global user_gen_counter
    user_gen_counter.clear()
    print("🔁 Лимиты генераций обнулены.")
