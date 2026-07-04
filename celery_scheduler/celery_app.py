from celery import Celery
from celery.schedules import crontab
from config.configurations import settings

app = Celery(
    "services",
    backend=settings.get_redis,
    broker=settings.get_redis,
    include=["celery_scheduler.tasks", "celery_scheduler.backgrounds.tasks", "celery_scheduler.posting.tasks"]
)

app.conf.beat_schedule = {
    "ai_news_parse": {
        "task": "tasks.parse_ai_news",
        "schedule": crontab(hour=20, minute=0)
    },
    "crypto_news_parse": {
        "task": "tasks.parse_crypto_news",
        "schedule": crontab(hour=2, minute=0)
    },
    "games_news_parse": {
        "task": "tasks.parse_games_news",
        "schedule": crontab(hour=22, minute=0)
    },
    "it_news_parse": {
        "task": "tasks.parse_it_news",
        "schedule": crontab(hour="4,14", minute=0)
    },
    "science_news_parse": {
        "task": "tasks.parse_science_news",
        "schedule": crontab(hour=0, minute=0)
    },
    "show_bis_news_parse": {
        "task": "tasks.parse_show_bis_news",
        "schedule": crontab(hour=12, minute=0)
    },
    "sport_news_parse": {
        "task": "tasks.parse_sports_news",
        "schedule": crontab(hour="10,18", minute=0)
    },
    "world_news_parse": {
        "task": "tasks.parse_world_news",
        "schedule": crontab(hour="8,16", minute=0)
    },
    "clean_old_parse_data": {
        "task": "tasks.clean_old_parse_data",
        "schedule": crontab(hour=3, minute=0)
    },
    "payment_plan_checker": {
        "task": "background.check_payment_plan",
        "schedule": crontab(hour=23, minute=57)
    },
    "set_default_posts_count": {
        "task": "background.set_default_post_count",
        "schedule": crontab(hour=0, minute=47)
    },
    "posting": {
        "task": "posting.posting",
        "schedule": crontab()
    },
    "clean_old_posted_data": {
        "task": "tasks.clean_old_posted_data",
        "schedule": crontab(hour=14, minute=47)
    },

}

app.conf.timezone = "Europe/Moscow"
