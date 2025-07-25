from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from bot.publisher import publish_scheduled_post
from bot.db.crud import reset_all_limits
from pytz import timezone


def setup_scheduler(bot):
    scheduler = AsyncIOScheduler()

    # Morning post
    scheduler.add_job(
        publish_scheduled_post,
        CronTrigger(hour=9, minute=00, timezone=timezone("Europe/Moscow")),
        kwargs={"bot": bot},
        name="Morning post",
    )

    # Midday post
    scheduler.add_job(
        publish_scheduled_post,
        CronTrigger(hour=14, minute=00, timezone=timezone("Europe/Moscow")),
        kwargs={"bot": bot},
        name="Midday post",
    )

    # Evening post
    scheduler.add_job(
        publish_scheduled_post,
        CronTrigger(hour=19, minute=00, timezone=timezone("Europe/Moscow")),
        kwargs={"bot": bot},
        name="Evening post",
    )

    # Reset Users /gen limits
    scheduler.add_job(
        reset_all_limits,
        CronTrigger(hour=0, minute=0, timezone=timezone("Europe/Moscow")),
        name="Reset /gen limits",
    )

    # Test
    # scheduler.add_job(
    #     publish_scheduled_post,
    #     CronTrigger(hour=11, minute=00, timezone=timezone("Europe/Moscow")),
    #     kwargs={"bot": bot},
    #     name="Test post",
    # )

    scheduler.start()
