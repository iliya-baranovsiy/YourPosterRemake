from business_logic.services.user_service import UserService
from business_logic.repositories.channels_db_repository import ChannelsDbRepository
from business_logic.repositories.channels_cache_repository import ChannelsCacheRepository


class ChannelsService:
    def __init__(self):
        self.user_rep = UserService()
        self.channel_repo = ChannelsDbRepository()
        self.channel_cache_repo = ChannelsCacheRepository()

    async def add_channel(self, owner_id: int, channel_id: int, channel_name: str):
        channel_exists = await self.channel_cache_repo.check_existing(channel_id=channel_id)
        if channel_exists:
            return
        channel_in_db = await self.channel_repo.check_channel_existing(channel_id=channel_id)
        if channel_in_db:
            # add lost cache
            return
        await self.channel_repo.add_channel(channel_id=channel_id, channel_name=channel_name, owner_id=owner_id)
        await self.channel_cache_repo.add_channel(channel_id=channel_id, owner_id=owner_id, channel_name=channel_name)

    async def get_channels(self, owner_id: int):
        channels_in_cache = await self.channel_cache_repo.get_user_channels(owner_id=owner_id)
        if channels_in_cache:
            return channels_in_cache
        channels_in_db = await self.channel_repo.get_channels(owner_id=owner_id)
        if channels_in_db:
            # add lost cache
            return channels_in_db
        else:
            return None

    async def delete_channel(self, channel_id: int, owner_id: int):
        await self.channel_repo.delete_channel(channel_id=channel_id)
        await self.channel_cache_repo.delete_channel(channel_id=channel_id, owner_id=owner_id)
