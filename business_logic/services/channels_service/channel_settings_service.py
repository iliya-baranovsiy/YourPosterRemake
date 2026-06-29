from business_logic.repositories.channels_db_repository import ChannelsDbRepository
from business_logic.repositories.channels_cache_repository import ChannelsCacheRepository
from business_logic.entities.channel_entity import ChannelSettings
from business_logic.services.user_service import UserService
from database.payments.options import PLAN_INFO


class ChannelSettingsService:
    def __init__(self):
        self.cache = ChannelsCacheRepository()
        self.db_rep = ChannelsDbRepository()
        self.user = UserService()

    async def get_channel_settings(self, channel_id: int, tg_id: int) -> ChannelSettings:
        settings = await self.cache.get_channel_settings(channel_id=channel_id)
        if not settings:
            settings = await self.db_rep.get_channel_settings(channel_id=channel_id)
            if settings:
                await self.cache.add_channel_settings(channel_id=settings.channel_id,
                                                      channel_name=settings.channel_name,
                                                      time=settings.time,
                                                      theme=settings.theme,
                                                      posts_count=settings.posts_count,
                                                      resource=settings.resource, )
        payment_plan = await self.user.get_only_payment_plan(tg_id=tg_id)
        settings.posts_available_count = PLAN_INFO[payment_plan].posts_count
        return settings

    async def update_channel_settings(self, channel: ChannelSettings):
        await self.db_rep.update_channel_settings(channel=channel)
        await self.cache.update_settings_cache(channel=channel)

    async def update_channel_time(self, channel: ChannelSettings):
        await self.db_rep.update_channel_times(channel=channel)
        await self.cache.update_settings_cache(channel=channel)
