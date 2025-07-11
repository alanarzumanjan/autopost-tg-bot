from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from bot.publisher import publish_scheduled_post
from pytz import timezone

def setup_scheduler(bot):
    scheduler = AsyncIOScheduler()

    # First post in Morning
    scheduler.add_job(
        publish_scheduled_post,
        CronTrigger(hour=9, minute=00,timezone=timezone("Europe/Moscow")),
        kwargs={"bot": bot},
        name="Morning post"
    )

    # Second post in Evening
    scheduler.add_job(
        publish_scheduled_post,
        CronTrigger(hour=19, minute=57,timezone=timezone("Europe/Moscow")),
        kwargs={"bot": bot},
        name="Evening post"
    )

    # Test
    scheduler.add_job(
        publish_scheduled_post,
        CronTrigger(hour=19, minute=44,timezone=timezone("Europe/Moscow")),
        kwargs={"bot": bot},
        name="Test post"
    )
    
    scheduler.add_job(
        publish_scheduled_post,
        CronTrigger(hour=20, minute=2,timezone=timezone("Europe/Moscow")),
        kwargs={"bot": bot},
        name="Test post"
    )

    scheduler.add_job(
        publish_scheduled_post,
        CronTrigger(hour=20, minute=6,timezone=timezone("Europe/Moscow")),
        kwargs={"bot": bot},
        name="Test post"
    )

    scheduler.start()