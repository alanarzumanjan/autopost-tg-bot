from aiogram import Bot
from bot.db.crud import get_scheduled_post, mark_post_as_published
from datetime import datetime, timezone

CHANNEL_ID = -1002768447325

async def publish_scheduled_post(bot: Bot):
    print("🕓 Задача публикации запущена...")
    post = get_scheduled_post()
    if not post:
        print(f"📦 Найден пост: {post.title if post else 'нет поста'}")
        return
    
    should_post = False
    if not post.scheduled_for:
         should_post = True
    else:
        now = datetime.utcnow()
        scheduled_naive = post.scheduled_for.replace(tzinfo=None)
        should_post = scheduled_naive <= now
        print(f"⏱ scheduled_for = {scheduled_naive}, now = {now}, ready = {should_post}")
    
    if should_post:
            try:
                message = f"📝 {post.title}\n\n{post.content}"
                print("📨 Отправка сообщения в канал...")
                await bot.send_message(CHANNEL_ID, message)
                mark_post_as_published(post.id)
                print(f"📝 Post {post.title} is published!")
            except Exception as e:
                print(f"❌ Error in sending post: {e}")
    else:
         print("⏳ Время публикации ещё не наступило.")