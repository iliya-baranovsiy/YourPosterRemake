from cache.app_cache.extension_cache import ExtensionCache
from business_logic.entities.channel_entity import Resource
from mongo.mongo_cache_worker import MongoExceptionWork
from exceptions.redis_exception_services.decorators import cache_exception


class ExtensionFileCacheRepository:
    def __init__(self):
        self.cache = ExtensionCache(type_=Resource.FILE)
        self.mongo = MongoExceptionWork()

    @cache_exception("channel_id", default_return=None)
    async def add_count(self, channel_id: int, count: int):
        await self.cache.add_count(channel_id=channel_id, count=count)

    @cache_exception("channel_id", default_return=None)
    async def get_count(self, channel_id: int):
        count = await self.cache.get_count(channel_id=channel_id)
        return count["records_count"] if count is not None else None

    @cache_exception("channel_id", default_return=None)
    async def delete_posts_count(self, channel_id: int):
        await self.cache.delete_posts_count(channel_id=channel_id)
