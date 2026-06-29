from cache.app_cache.extension_cache import ExtensionCache
from business_logic.entities.channel_entity import Resource


class ExtensionFileCacheRepository:
    def __init__(self):
        self.cache = ExtensionCache(type_=Resource.FILE)

    async def add_count(self, channel_id: int, count: int):
        await self.cache.add_count(channel_id=channel_id, count=count)

    async def get_count(self, channel_id: int):
        count = await self.cache.get_count(channel_id=channel_id)
        return count["records_count"] if count is not None else None
