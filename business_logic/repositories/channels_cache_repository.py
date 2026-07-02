from cache.app_cache.channels_cache import ChannelsCache
from business_logic.entities.channel_entity import PostTheme, Resource, BaseChannelInfo, ChannelSettings
from mongo.mongo_cache_worker import MongoExceptionWork
from exceptions.redis_exception_services.decorators import cache_exception


class ChannelsCacheRepository:
    def __init__(self):
        self.channels_cache = ChannelsCache()
        self.mongo = MongoExceptionWork()

    @cache_exception("channel_id", "owner_id", default_return=None)
    async def add_channel(self,
                          channel_id: int,
                          owner_id: int,
                          channel_name: str):
        await self.channels_cache.add_channel(
            channel_id=channel_id,
            channel_name=channel_name,
            owner_id=owner_id)

    @cache_exception("channel_id", default_return=None)
    async def add_channel_settings(self,
                                   channel_id: int,
                                   channel_name: str,
                                   time: list[str] | None = None,
                                   posts_count: int = 0,
                                   theme: PostTheme = PostTheme.UNDEFINED,
                                   posting_is_active: bool = False,
                                   resource: Resource = Resource.DATABASE, ):
        await self.channels_cache.add_channel_settings(
            channel_id=channel_id,
            channel_name=channel_name,
            posts_count=posts_count,
            theme=theme.value,
            time=time,
            posting_is_active=posting_is_active,
            resource=resource.value, )

    @cache_exception("owner_id", default_return=[])
    async def get_user_channels(self, owner_id: int) -> list:
        data = await self.channels_cache.get_user_channels(owner_id=owner_id)
        if data:
            result = []
            for key, value in data.items():
                result.append(BaseChannelInfo(channel_id=int(key), channel_name=value))
            return result
        return []

    @cache_exception("channel_id", default_return=None)
    async def get_channel_settings(self, channel_id: int):
        data = await self.channels_cache.get_channel_settings(channel_id=channel_id)
        if data:
            settings = ChannelSettings(channel_id=channel_id,
                                       channel_name=data["channel_name"],
                                       posts_count=data["posts_count"],
                                       posts_available_count=0,
                                       theme=PostTheme(data["theme"]),
                                       resource=Resource(data["resource"]),
                                       time=data["time"],
                                       posting_is_active=data["posting_is_active"]
                                       )
            return settings
        return None

    @cache_exception("channel.channel_id", default_return=None)
    async def update_settings_cache(self, channel: ChannelSettings):
        await self.add_channel_settings(
            channel_id=channel.channel_id,
            channel_name=channel.channel_name,
            posts_count=channel.posts_count,
            theme=channel.theme,
            posting_is_active=channel.posting_is_active,
            resource=channel.resource,
            time=channel.time,
        )

    @cache_exception("channel_id", default_return=False)
    async def check_existing(self, channel_id: int) -> bool:
        existing = await self.channels_cache.check_channel_existing(channel_id=channel_id)
        return existing

    @cache_exception("channel_id", "owner_id", default_return=None)
    async def delete_channel(self, owner_id: int, channel_id: int):
        await self.channels_cache.delete_channel(owner_id=owner_id, channel_id=channel_id)

    @cache_exception("channel_id", "owner_id", default_return=None)
    async def add_lost_cache(self, channel_id: int, owner_id: int, channel_name: str):
        await self.add_channel(channel_id=channel_id, owner_id=owner_id, channel_name=channel_name)

    @cache_exception("channel_id", default_return=None)
    async def delete_channel_fields(self, channel_id: int):
        await self.channels_cache.delete_by_channel_id(channel_id=channel_id)

    @cache_exception("user_id", default_return=None)
    async def delete_user_fields(self, user_id: int):
        await self.channels_cache.delete_by_tg_id(tg_id=user_id)
