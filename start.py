import asyncio
from botLogic.main_bot import start_bot as bot
from background_services.redis_exception_checker import redis_checker


async def main():
    await asyncio.gather(
        bot(),
        redis_checker.check_redis_work(),
    )


if __name__ == "__main__":
    asyncio.run(main())
