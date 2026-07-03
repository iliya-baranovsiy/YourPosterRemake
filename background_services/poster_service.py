from datetime import datetime

from database.backgroundt_tasks_db.orm import BackGroundTasksORM
from business_logic.services.channels_service.channel_settings_service import ChannelSettingsService
from business_logic.services.user_service import UserService
from botLogic.bot_services.bot_instance import bot
from database.payments.options import PLAN_INFO
from business_logic.entities.channel_entity import Resource
from business_logic.services.channels_service.extension_service import ExtensionService
from database.extension_db.models import FileUserModel
from database.extension_db.orm import ExtensionOrm


class Poster:
    def __init__(self):
        self.orm = BackGroundTasksORM()
        self.channel_service = ChannelSettingsService()
        self.user_service = UserService()
        self.ext_service = ExtensionService()
        self.ext_orm = ExtensionOrm()
        self.bot = bot

    async def make_post(self):
        current_time = datetime.now().time().strftime("%H:%M")
        channels_ids = await self.orm.get_current_channel_ids(current_time=current_time)
        for tup in channels_ids:
            channel = await self.channel_service.get_channel_settings(channel_id=tup[0], tg_id=tup[1])
            payment = await self.user_service.get_only_payment_plan(tg_id=tup[1])
            if channel.posting_is_active:
                if channel.posts_count < PLAN_INFO[payment].posts_count:
                    count = await self.ext_service.get_file_posts_count(channel_id=tup[0])
                    if channel.resource == Resource.FILE:
                        if count > 0:
                            post_data = await self.orm.get_file_post(channel_id=tup[0])
                            try:
                                await bot.send_message(chat_id=tup[0], text=f"<b>{post_data[0]}</b>\n{post_data[1]}")
                                channel.posts_count += 1
                                await self.channel_service.update_channel_settings(channel=channel)
                                await self.ext_service.update_records_count(channel_id=tup[0], count=count - 1)
                                await self.ext_orm.delete_target_record(channel_id=tup[0], title=post_data[0],
                                                                        table=FileUserModel)
                            except:
                                continue
                        else:
                            continue
                    else:
                        pass
                else:
                    continue
            else:
                continue
