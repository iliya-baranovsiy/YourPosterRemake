from datetime import datetime

from database.backgroundt_tasks_db.orm import BackGroundTasksORM
from business_logic.services.channels_service.channel_settings_service import ChannelSettingsService
from botLogic.bot_services.bot_instance import bot


class Poster:
    def __init__(self):
        self.orm = BackGroundTasksORM()
        self.channel_service = ChannelSettingsService()
        self.bot = bot

    async def make_post(self):
        current_time = datetime.now().time().strftime("%H:%M")
        channels_ids = await self.orm.get_current_channel_ids(current_time=current_time)
