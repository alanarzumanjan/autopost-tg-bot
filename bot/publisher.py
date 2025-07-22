from aiogram import Bot
from bot.db.crud import get_scheduled_post, mark_post_as_published, add_post
from datetime import datetime
from bot.generator.generator import generate_post
import re

from bot.config import CHANNEL_ID


def clean_markdown(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = text.replace("\u200b", "")
    text = text.replace("\u202f", " ")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def clean_html(text: str) -> str:
    # Telegram НЕ поддерживает <p>, <br>, <ul>, <li> и т.п.
    text = re.sub(r"</?p>", "", text)
    text = re.sub(r"</?br\s*/?>", "\n", text)
    return text.strip()


async def publish_scheduled_post(bot: Bot):
    print("🕓 Задача публикации запущена...")

    post = get_scheduled_post()

    if not post:
        print("📭 В базе нет готового поста. Пробуем сгенерировать...")
        try:
            content = await generate_post(bot=bot)
        except Exception as e:
            print(f"❌ Ошибка при обращении к OpenAI: {e}")
            return

        if content:
            post = add_post(
                title="AI generated",
                content=content,
                scheduled_for=datetime.utcnow(),
                is_ai_generated=True,
            )
            print("✅ Пост успешно сгенерирован и сохранён.")
        else:
            print("❌ Не удалось сгенерировать пост (пустой ответ).")
            return

    should_post = False
    if not post.scheduled_for:
        should_post = True
    else:
        now = datetime.utcnow()
        scheduled_naive = post.scheduled_for.replace(tzinfo=None)
        should_post = scheduled_naive <= now
        print(
            f"⏱ scheduled_for = {scheduled_naive}, now = {now}, ready = {should_post}"
        )

    if should_post:
        try:
            cleaned = clean_html(post.content)
            print("📨 Отправка сообщения в канал...")
            await bot.send_message(CHANNEL_ID, cleaned, parse_mode="HTML")
            mark_post_as_published(post.id)
            print(f"✅ Пост опубликован: {post.title}")
        except Exception as e:
            print(f"❌ Ошибка отправки поста: {e}")
    else:
        print("⏳ Время публикации ещё не наступило.")
