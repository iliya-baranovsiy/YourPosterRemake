from business_logic.repositories.extension_repository import ExtensionFileRepository
from business_logic.services.channels_service.channel_settings_service import ChannelSettingsService
from business_logic.common_options.status_option import Status


class ExtensionService:
    def __init__(self):
        self.rep = ExtensionFileRepository()
        self.channel_settings = ChannelSettingsService()

    async def add_file_records(self, channel_id: int, tg_id: int, records: list[dict]) -> Status:
        settings = await self.channel_settings.get_channel_settings(channel_id=channel_id, tg_id=tg_id)
        if settings.file_posts_count < 31:
            try:
                await self.rep.add_file_records(records=records)
                count = await self.rep.get_file_posts_count(channel_id=channel_id)
                settings.file_posts_count = count
                await self.channel_settings.update_file_posts_count(settings)
                return Status.OK
            except:
                return Status.BAD
        else:
            return Status.BAD

    async def delete_file_records(self, channel_id: int, tg_id: int) -> Status:
        try:
            await self.rep.delete_file_records(channel_id=channel_id)
            channel = await self.channel_settings.get_channel_settings(channel_id=channel_id, tg_id=tg_id)
            channel.file_posts_count = 0
            await self.channel_settings.update_file_posts_count(channel=channel)
            return Status.OK
        except Exception as e:
            print(e)
            return Status.BAD

    async def request_to_load_file(self, channel_id: int, tg_id: int) -> Status:
        channel = await self.channel_settings.get_channel_settings(channel_id=channel_id, tg_id=tg_id)
        if channel.file_posts_count < 31:
            return Status.OK
        else:
            return Status.BAD
