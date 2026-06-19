from sqlalchemy import select
from .models import ChannelsModel
from ..engines import async_session


class ChannelsOrm:

    @staticmethod
    async def get_user_channels(tg_id: int):
        async with async_session() as session:
            query = select(ChannelsModel.channel_id, ChannelsModel.title).where(ChannelsModel.owner_id == tg_id)
            executing = await session.execute(query)
            result = executing.scalars().all()
            print(result)
