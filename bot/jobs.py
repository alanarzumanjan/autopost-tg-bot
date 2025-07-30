from bot.db.session import SessionLocal
from bot.db.models import UserChannel
import json
from bot.publisher import publish_scheduled_post
from apscheduler.triggers.cron import CronTrigger
from pytz import timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler


def setup_scheduler(bot):
    scheduler = AsyncIOScheduler()

    db = SessionLocal()
    channels = db.query(UserChannel).filter_by(is_active=True).all()
    db.close()

    for channel in channels:
        if hasattr(channel, "get_post_times"):
            times = channel.get_post_times()
        else:
            times = channel.post_times or []

        for idx, t in enumerate(times):
            try:
                hour, minute = map(int, t.split(":"))
                scheduler.add_job(
                    publish_scheduled_post,
                    CronTrigger(
                        hour=hour, minute=minute, timezone=timezone("Europe/Moscow")
                    ),
                    kwargs={"bot": bot},
                    name=f"{channel.tg_channel_id}_{t}",
                )
                print(f"🕒 План публикации: {channel.tg_channel_id} в {t}")
            except Exception as e:
                print(f"❌ Ошибка планирования для {channel.tg_channel_id}: {e}")

    scheduler.start()
