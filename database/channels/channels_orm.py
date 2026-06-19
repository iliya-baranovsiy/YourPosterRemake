from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from .models import ChannelsModel, ChannelsSettingsModel
from ..engines import async_session


class ChannelsOrm:

    @staticmethod
    async def get_user_channels(tg_id: int):
        async with async_session() as session:
            query = select(ChannelsModel.channel_id, ChannelsModel.title).where(ChannelsModel.owner_id == tg_id)
            executing = await session.execute(query)
            result = executing.all()
            return result

    @staticmethod
    async def add_channel(channel_id: int,
                          channel_title: str,
                          owner_id: int):
        async with async_session() as session:
            insert_channel = insert(ChannelsModel).values(
                channel_id=channel_id,
                title=channel_title,
                owner_id=owner_id,
            )
            insert_channel_settings = insert(ChannelsSettingsModel).values(
                channel_id=channel_id
            )
            unique_insert_channel_settings = insert_channel_settings.on_conflict_do_nothing(
                index_elements=["channel_id"])
            unique_channel = insert_channel.on_conflict_do_nothing(index_elements=["channel_id"])
            async with session.begin():
                await session.execute(unique_channel)
                await session.execute(unique_insert_channel_settings)
