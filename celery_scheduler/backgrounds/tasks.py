import asyncio
from ..celery_app import app
from background_services.check_payment_plan import CheckPaymentPlan


@app.task(name="background.check_payment_plan", queue="background_tasks")
def handle_payment_plan():
    asyncio.run(CheckPaymentPlan().update_plan())
