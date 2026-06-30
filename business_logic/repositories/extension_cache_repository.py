from cache.app_cache.extension_cache import ExtensionCache
from business_logic.entities.channel_entity import Resource
from mongo.mongo_cache_worker import MongoExceptionWork
from events.redis_exeption_event import redis_exception


class ExtensionFileCacheRepository:
    def __init__(self):
        self.cache = ExtensionCache(type_=Resource.FILE)
        self.mongo = MongoExceptionWork()

    async def add_count(self, channel_id: int, count: int):
        try:
            await self.cache.add_count(channel_id=channel_id, count=count)
        except:
            await self.mongo.write_id(id_=channel_id)
            redis_exception.set()

    async def get_count(self, channel_id: int):
        try:
            count = await self.cache.get_count(channel_id=channel_id)
            return count["records_count"] if count is not None else None
        except:
            await self.mongo.write_id(id_=channel_id)
            redis_exception.set()
            return None

    async def delete_posts_count(self, channel_id: int):
        try:
            await self.cache.delete_posts_count(channel_id=channel_id)
        except:
            await self.mongo.write_id(id_=channel_id)
            redis_exception.set()
