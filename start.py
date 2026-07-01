import asyncio
from botLogic.main_bot import start_bot as bot
from background_services.redis_exception_checker import redis_checker
from mongo.mongo_cache_worker import MongoExceptionWork


async def main():
    await asyncio.gather(
        bot(),
        redis_checker.check_redis_work(),
        MongoExceptionWork().create_mongo_index(),
    )


if __name__ == "__main__":
    asyncio.run(main())
