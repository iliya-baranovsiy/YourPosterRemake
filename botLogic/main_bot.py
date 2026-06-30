from fastapi import FastAPI, Request
from botLogic.bot_services.app_instance import dp, WEBHOOK_PATH, WEBHOOK_URL
from botLogic.bot_services.bot_instance import bot
import contextlib
import uvicorn
import asyncio

from cache.app_cache.user_cache import UserCache  # delete
from cache.app_cache.channels_cache import ChannelsCache  # delete
from cache.app_cache.extension_cache import ExtensionCache  # delete


@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(url=WEBHOOK_URL)
    yield
    await bot.session.close()


app = FastAPI(lifespan=lifespan)


@app.post(WEBHOOK_PATH)
async def bot_webhook(request: Request):
    update = await request.json()
    await dp.feed_webhook_update(bot=bot, update=update)
    return {"ok": True}


async def start_bot():
    await UserCache().clear_cache()  # delete
    await ChannelsCache().clear_channels_cache()  # delete
    await ExtensionCache().clear_count()  # delete
    conf = uvicorn.Config(
        app,
        host="127.0.0.1",
        port=8000,
        log_level="info",
        reload=True
    )
    server = uvicorn.Server(conf)
    await server.serve()
