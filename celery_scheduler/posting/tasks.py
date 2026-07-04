import asyncio
from ..celery_app import app
from background_services.poster_service import Poster

_loop = None


def get_loop():
    global _loop

    if _loop is None or _loop.is_closed():
        _loop = asyncio.new_event_loop()

    return _loop


@app.task(name="posting.posting", queue="posting_tasks")
def posting():
    loop = get_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(run_posting())


async def run_posting():
    poster = Poster()
    await poster.start_posting()
