from business_logic.repositories.extension_repository import ExtensionFileRepository
from business_logic.services.channels_service.channel_settings_service import ChannelSettingsService
from business_logic.common_options.status_option import Status
from business_logic.repositories.extension_cache_repository import ExtensionFileCacheRepository
from business_logic.entities.channel_entity import Resource


class ExtensionService:
    def __init__(self):
        self.rep = ExtensionFileRepository()
        self.cache = ExtensionFileCacheRepository()

    async def get_file_posts_count(self, channel_id):
        count = await self.cache.get_count(channel_id=channel_id)
        if count is None:
            count = await self.rep.get_file_posts_count(channel_id=channel_id)
            await self.cache.add_count(channel_id=channel_id, count=count)
        return count

    async def add_file_records(self, channel_id: int, records: list[dict]) -> Status:
        posts_count = await self.get_file_posts_count(channel_id=channel_id)
        if posts_count < 31:
            try:
                to_load_count = 31 - posts_count
                if len(records) > to_load_count:
                    records = records[:to_load_count]
                await self.rep.add_file_records(records=records)
                await self.cache.add_count(channel_id=channel_id, count=posts_count + len(records))
                return Status.OK
            except:
                return Status.BAD
        else:
            return Status.BAD

    async def delete_file_records(self, channel_id: int) -> Status:
        try:
            await self.rep.delete_file_records(channel_id=channel_id)
            await self.cache.add_count(channel_id=channel_id, count=0)
            return Status.OK
        except Exception as e:
            return Status.BAD

    async def request_to_load_file(self, channel_id: int) -> Status:
        posts_count = await self.get_file_posts_count(channel_id=channel_id)
        if posts_count < 31:
            return Status.OK
        else:
            return Status.BAD
