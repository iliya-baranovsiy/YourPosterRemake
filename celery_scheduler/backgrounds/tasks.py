import asyncio
from ..celery_app import app
from background_services.check_payment_plan import CheckPaymentPlan
from background_services.set_default_pc import DefaultPostsCountValue


@app.task(name="background.check_payment_plan", queue="background_tasks")
def handle_payment_plan():
    asyncio.run(CheckPaymentPlan().update_plan())


@app.task(name="background.set_default_post_count", queue="background_tasks")
def handle_set_default_posts_count():
    asyncio.run(DefaultPostsCountValue().set_default())
