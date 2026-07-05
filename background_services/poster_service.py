import asyncio
from datetime import datetime
from database.backgroundt_tasks_db.orm import BackGroundTasksORM
from business_logic.services.channels_service.channel_settings_service import ChannelSettingsService
from business_logic.services.user_service import UserService
from botLogic.bot_services.bot_instance import bot
from database.payments.options import PLAN_INFO
from business_logic.entities.channel_entity import Resource, PostTheme
from business_logic.services.channels_service.extension_service import ExtensionService
from database.extension_db.models import FileUserModel
from database.extension_db.orm import ExtensionOrm
from database.parse_db.models import AiNewsTable, ItTechnologiesTable, GamesTable, CryptoCurrencyTable, NewsTable, \
    SportTable, ShowBisTable, ScienceTable


class Poster:
    def __init__(self):
        self.orm = BackGroundTasksORM()
        self.channel_service = ChannelSettingsService()
        self.user_service = UserService()
        self.ext_service = ExtensionService()
        self.ext_orm = ExtensionOrm()
        self.bot = bot

    async def make_post(self, tup):
        channel = await self.channel_service.get_channel_settings(channel_id=tup[0], tg_id=tup[1])
        payment = await self.user_service.get_only_payment_plan(tg_id=tup[1])
        if channel.posting_is_active:
            if channel.posts_count < PLAN_INFO[payment].posts_count:
                if channel.resource == Resource.FILE:
                    count = await self.ext_service.get_file_posts_count(channel_id=tup[0])
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
                            pass
                    else:
                        pass
                else:
                    table = self.get_news_tabel(theme=channel.theme)
                    posted = await self.orm.get_channel_posted_titles(channel_id=tup[0])
                    for _ in range(3):
                        post = await self.orm.get_news_post(table)
                        if post:
                            if post[0] not in posted:
                                if post[2] is not None:
                                    try:
                                        caption = f"<b>{post[0]}</b>\n{post[1]}"
                                        await self.bot.send_photo(chat_id=tup[0],
                                                                  caption=caption,
                                                                  photo=post[2])
                                        await self.orm.insert_post_title(channel_id=tup[0], title=post[0])
                                        channel.posts_count += 1
                                        await self.channel_service.update_channel_settings(channel=channel)
                                        break
                                    except Exception as e:
                                        pass
                                else:
                                    try:
                                        caption = f"<b>{post[0]}</b>\n{post[1]}"
                                        await self.bot.send_message(chat_id=tup[0],
                                                                    text=caption)
                                        await self.orm.insert_post_title(channel_id=tup[0], title=post[0])
                                        channel.posts_count += 1
                                        await self.channel_service.update_channel_settings(channel=channel)
                                        break
                                    except Exception as e:
                                        break
                        else:
                            break
            else:
                pass
        else:
            pass

    async def start_posting(self):
        current_time = datetime.now().time().strftime("%H:%M")
        channels_ids = await self.orm.get_current_channel_ids(current_time=current_time)

        if not channels_ids:
            return
        semaphore = asyncio.Semaphore(10)

        async def worker(tup):
            async with semaphore:
                await self.make_post(tup)

        await asyncio.gather(*(worker(tup) for tup in channels_ids))

    def get_news_tabel(self, theme: PostTheme):
        match (theme):
            case PostTheme.AI_POSTS:
                return AiNewsTable
            case PostTheme.IT_NEWS:
                return ItTechnologiesTable
            case PostTheme.SPORT_NEWS:
                return SportTable
            case PostTheme.SCIENCE_NEWS:
                return ScienceTable
            case PostTheme.SHOW_BIS_NEWS:
                return ShowBisTable
            case PostTheme.WORLD_NEWS:
                return NewsTable
            case PostTheme.CRYPTO_NEWS:
                return CryptoCurrencyTable
            case PostTheme.GAMES_NEWS:
                return GamesTable
