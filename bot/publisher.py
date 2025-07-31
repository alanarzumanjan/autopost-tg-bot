from aiogram import Bot
from datetime import datetime
from bot.db.crud import mark_post_as_published, add_post, record_post_send
from bot.generator.generator import generate_post
import re


def clean_html(text: str) -> str:
    text = re.sub(r"</?p>", "", text)
    text = re.sub(r"</?br\s*/?>", "\n", text)
    return text.strip()


async def publish_scheduled_post(bot: Bot, channel):
    print(f"\n🕓 Публикация для {channel.tg_channel_id}...")

    try:
        content = await generate_post(
            bot=bot,
            custom_prompt=channel.custom_prompt,
            template=getattr(channel, "template", "smart"),
        )
    except Exception as e:
        print(f"❌ Ошибка генерации для {channel.tg_channel_id}: {e}")
        return

    if not content:
        print(f"❌ Пустой результат генерации для {channel.tg_channel_id}.")
        return

    post = add_post(
        title="AI generated",
        content=content,
        scheduled_for=datetime.utcnow(),
        is_ai_generated=True,
    )

    try:
        cleaned = clean_html(post.content)
        await bot.send_message(channel.tg_channel_id, cleaned, parse_mode="HTML")
        mark_post_as_published(post.id)
        record_post_send(post.id, channel.id)
        print(f"✅ Пост отправлен в {channel.tg_channel_id}")

        # 📦 Логирование
        now = datetime.utcnow().isoformat()
        log_entry = (
            f"[{now}] POSTED to {channel.tg_channel_id} ({channel.title}) | "
            f"Post ID: {post.id} | Tokens: ~{len(cleaned.split())} words | "
            f"Template: {getattr(channel, 'template', 'smart')}\n" + "-" * 60 + "\n"
        )
        with open("posting_log.txt", "a", encoding="utf-8") as f:
            f.write(log_entry)

        print(f"✅ Пост отправлен в {channel.tg_channel_id}")

    except Exception as e:
        print(f"❌ Ошибка отправки в {channel.tg_channel_id}: {e}")
