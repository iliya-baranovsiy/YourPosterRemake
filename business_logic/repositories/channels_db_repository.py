from database.channels.channels_orm import ChannelsOrm
from business_logic.entities.channel_entity import BaseChannelInfo


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

    async def check_channel_existing(self, channel_id: int) -> bool:
        existing = await self.channels_orm.check_channel_existing(channel_id=channel_id)
        return existing

    async def update_channel_settings(self):
        pass

    async def delete_channel(self, channel_id: int):
        await self.channels_orm.delete_channel(channel_id=channel_id)
