from aiogram import Bot
from bot.db.crud import get_sheduled_post, mark_post_as_publiched
from datetime import datetime

CHANNEL_ID = -1002768447325

async def publish_scheduled_post(bot: Bot):
    post = get_sheduled_post()
    if post and (not post.scheduled_for or post.scheduled_for <= datetime.utcnow()):
        try:
            message = f"📝 {post.title or "New Post"}\n\n{post.content}"
            await bot.send_message(CHANNEL_ID, message)
            mark_post_as_publiched(post.id)
        except Exception as e:
            print(f"Error in sending post: {e}")