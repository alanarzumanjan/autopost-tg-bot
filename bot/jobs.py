from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from bot.publisher import publish_scheduled_post
from pytz import timezone

def setup_scheduler(bot):
    scheduler = AsyncIOScheduler()

    # Every day in time post
    scheduler.add_job(
        publish_scheduled_post,
        CronTrigger(hour=19, minute=33,timezone=timezone("Europe/Moscow")),
        kwargs={"bot": bot},
        name="Daily post publishing"
    )

    scheduler.start()