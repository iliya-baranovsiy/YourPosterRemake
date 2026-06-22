from database.channels.channels_orm import ChannelsOrm
from business_logic.entities.channel_entity import BaseChannelInfo, ChannelSettings


class ChannelsDbRepository:
    def __init__(self):
        self.channels_orm = ChannelsOrm()

    async def add_channel(self, channel_id: int, owner_id: int, channel_name: str):
        await self.channels_orm.add_channel(channel_id=channel_id, owner_id=owner_id, channel_title=channel_name)

    async def get_channels(self, owner_id: int) -> list:
        data = await self.channels_orm.get_user_channels(tg_id=owner_id)
        if data:
            result_list = []
            for i in data:
                result_list.append(BaseChannelInfo(channel_id=i[0], channel_name=i[1]))
            return result_list
        return []

    async def get_channel_settings(self, channel_id: int):
        data = await self.channels_orm.get_channel_settings(channel_id=channel_id)
        settings = ChannelSettings(channel_id=channel_id,
                                   channel_name=data.channel_name,
                                   posts_count=data.post_count,
                                   posts_available_count=data.post_available_count,
                                   posting_is_active=data.is_active_posting,
                                   theme=data.post_theme,
                                   resource=data.posts_resource,
                                   time=data.posts_times)
        return settings

    async def check_channel_existing(self, channel_id: int) -> bool:
        existing = await self.channels_orm.check_channel_existing(channel_id=channel_id)
        return existing

    async def update_channel_settings(self, channel: ChannelSettings):
        await self.channels_orm.update_channel_settings(
            channel_id=channel.channel_id,
            posts_available_count=channel.posts_available_count,
            posts_count=channel.posts_count,
            theme=channel.theme,
            is_active_posting=channel.posting_is_active,
            resource=channel.resource
        )

    async def delete_channel(self, channel_id: int):
        await self.channels_orm.delete_channel(channel_id=channel_id)
