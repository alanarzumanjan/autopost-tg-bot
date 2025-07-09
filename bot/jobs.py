from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from bot.services.publisher import publish_scheduled_post

def setup_scheduler(bot):
    scheduler = AsyncIOScheduler()

    # Every day in 10:00 UTC
    scheduler.add_job(
        publish_scheduled_post,
        CronTrigger(hour=10,minute=0),
        kwargs={"bot": bot},
        name="Daily post publishing"
    )
    
    scheduler.start()