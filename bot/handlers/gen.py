from aiogram import types
from aiogram.dispatcher import Dispatcher
from bot.generator.generator import generate_post
from bot.db.crud import get_user_limit, increment_user_limit


max_gen_per_user = 3


async def gen_handler(message: types.Message):
    await message.answer("""
        Example: /gen Write post about Women Style
    """)

    user_id = message.from_user.id
    text = message.get_args().strip()
    custom_prompt = text if text else None
    print(
        f"👉 /gen вызван пользователем {user_id} с аргументами: {text}, {custom_prompt}"
    )

    count = get_user_limit(user_id)
    if count >= max_gen_per_user:
        await message.reply("🚫 Вы достигли лимита генераций (3). Попробуйте завтра.")
        return

    await message.reply("⏳ Генерирую пост...")

    post = await generate_post(custom_prompt=custom_prompt)

    if post:
        await message.answer(post, parse_mode="HTML")
        increment_user_limit(user_id)
    else:
        await message.answer("❌ Не удалось сгенерировать пост.")


def register_gen_handler(dp: Dispatcher):
    dp.register_message_handler(gen_handler, commands=["gen"])


def reset_generation_limits():
    global user_gen_counter
    user_gen_counter.clear()
    print("🔁 Лимиты генераций обнулены.")
