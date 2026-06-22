from business_logic.repositories.channels_db_repository import ChannelsDbRepository
from business_logic.repositories.channels_cache_repository import ChannelsCacheRepository


class ChannelSettingsService:
    def __init__(self):
        self.cache = ChannelsCacheRepository()
        self.db_rep = ChannelsDbRepository()

    async def get_channel_settings(self, channel_id: int):
        settings = await self.cache.get_channel_settings(channel_id=channel_id)
        if not settings:
            settings = await self.db_rep.get_channel_settings(channel_id=channel_id)
            if settings:
                await self.cache.add_channel_settings(channel_id=settings.channel_id,
                                                      channel_name=settings.channel_name,
                                                      time=settings.time,
                                                      theme=settings.theme,
                                                      posts_count=settings.posts_count,
                                                      posts_available_count=settings.posts_available_count)
        return settings
