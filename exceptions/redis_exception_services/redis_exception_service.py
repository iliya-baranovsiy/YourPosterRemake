from business_logic.repositories.channels_cache_repository import ChannelsCacheRepository
from business_logic.repositories.extension_cache_repository import ExtensionFileCacheRepository
from business_logic.repositories.user_cache_repository import UserCacheRepository
from mongo.mongo_cache_worker import MongoExceptionWork


class RedisExceptionService:
    def __init__(self):
        self._user_cache = UserCacheRepository()
        self._channel_cache = ChannelsCacheRepository()
        self._extension_file_cache = ExtensionFileCacheRepository()
        self.mongo = MongoExceptionWork()

    async def clear_cache(self, id_list: list):
        for id_ in id_list:
            if id_ < 0:
                await self._channel_cache.delete_channel_fields(channel_id=id_)
                await self._extension_file_cache.delete_posts_count(channel_id=id_)
            else:
                await self._user_cache.delete_user_cache(user_id=id_)
                await self._channel_cache.delete_user_fields(user_id=id_)
            await self.mongo.delete_id(id_=id_)
