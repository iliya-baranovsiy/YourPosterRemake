import asyncio

from cache.redis_instance import redis_engine
from mongo.mongo_cache_worker import MongoExceptionWork
from exceptions.redis_exception_services.redis_exception_service import RedisExceptionService
from events.redis_exeption_event import redis_exception


class RedisChecker:
    def __init__(self):
        self.mongo = MongoExceptionWork()
        self.redis = RedisExceptionService()

    async def check_redis_work(self):
        while True:
            await redis_exception.wait()
            exceptions_ids = await self.mongo.get_all_ids()
            if exceptions_ids:
                try:
                    await redis_engine.ping()
                    await self.redis.clear_cache(exceptions_ids)

                except:
                    await asyncio.sleep(3)
                    continue
            redis_exception.clear()


redis_checker = RedisChecker()
