from aiogram import Bot
from bot.db.crud import (
    get_scheduled_post,
    mark_post_as_published,
    add_post,
    was_post_sent,
    record_post_send,
)
from datetime import datetime
from bot.generator.generator import generate_post
from bot.db.session import SessionLocal
from bot.db.models import UserChannel
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

    db = SessionLocal()
    channels = db.query(UserChannel).filter_by(is_active=True).all()
    db.close()

    if not channels:
        print("📭 Нет активных каналов.")
        return

    async def publish_scheduled_post(bot: Bot):
        print("🕓 Задача публикации запущена...")

        db = SessionLocal()
        channels = db.query(UserChannel).filter_by(is_active=True).all()
        db.close()

        if not channels:
            print("📭 Нет активных каналов.")
            return

        for channel in channels:
            print(f"\n➡ Генерация поста для {channel.tg_channel_id}")

            try:
                content = await generate_post(
                    bot=bot, custom_prompt=channel.custom_prompt
                )
            except Exception as e:
                print(f"❌ Ошибка генерации для {channel.tg_channel_id}: {e}")
                continue

            if not content:
                print("❌ Пустой результат генерации.")
                continue

            post = add_post(
                title="AI generated",
                content=content,
                scheduled_for=datetime.utcnow(),
                is_ai_generated=True,
            )

            should_post = (
                not post.scheduled_for
                or post.scheduled_for.replace(tzinfo=None) <= datetime.utcnow()
            )

            if was_post_sent(post.id, channel.id):
                print(
                    f"⏩ Пост {post.id} уже отправлен в {channel.tg_channel_id}. Пропускаем."
                )
                continue

            if should_post:
                try:
                    cleaned = clean_html(post.content)
                    print(f"📨 Отправка в {channel.tg_channel_id}...")
                    await bot.send_message(
                        channel.tg_channel_id, cleaned, parse_mode="HTML"
                    )
                    mark_post_as_published(post.id)
                    record_post_send(post.id, channel.id)
                    print(f"✅ Успешно отправлен и записан.")
                except Exception as e:
                    print(f"❌ Ошибка при отправке в {channel.tg_channel_id}: {e}")
            else:
                print(f"⏳ Время публикации для {channel.tg_channel_id} ещё не пришло.")
