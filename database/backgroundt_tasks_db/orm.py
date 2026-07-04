from datetime import date
from sqlalchemy import select, update, delete, func
from sqlalchemy.dialects.postgresql import insert

from ..engines import async_session
from ..payments.models import PaymentModel
from database.channels.models import ChannelsSettingsModel, PostsTimesModel
from database.parse_db.models import PostedTable
from database.channels.models import ChannelsModel
from database.extension_db.models import FileUserModel


class BackGroundTasksORM:

    @staticmethod
    async def get_payments_ids(today: date) -> list:
        async with async_session() as session:
            res = await session.execute(
                select(PaymentModel.user_id).where(
                    PaymentModel.end_date == today
                )
            )
            return res.scalars().all()

    @staticmethod
    async def set_default_posts_count():
        async with async_session() as session:
            stmt = update(ChannelsSettingsModel).values(
                posts_count=0
            )
            async with session.begin():
                await session.execute(stmt)

    @staticmethod
    async def get_current_channel_ids(current_time: str) -> list:
        async with async_session() as session:
            res = await session.execute(
                select(
                    PostsTimesModel.channel_id,
                    ChannelsModel.owner_id
                )
                .join(
                    ChannelsModel,
                    PostsTimesModel.channel_id == ChannelsModel.channel_id
                )
                .where(
                    PostsTimesModel.time == current_time
                )
            )
            return res.all()

    @staticmethod
    async def insert_post_title(channel_id: int, title: str):
        async with async_session() as session:
            stmt = insert(PostedTable).values(
                channel_id=channel_id,
                title=title
            )
            async with session.begin():
                await session.execute(stmt)

    @staticmethod
    async def get_channel_posted_titles(channel_id: int):
        async with (async_session() as session):
            res = await session.execute(
                select(PostedTable.title).where(
                    PostedTable.channel_id == channel_id
                )
            )
            return res.scalars().all()

    @staticmethod
    async def delete_old_posted_titles(posted_date: date):
        async with async_session() as session:
            await session.execute(delete(PostedTable).where(
                PostedTable.post_date == posted_date
            )
            )
            await session.commit()

    @staticmethod
    async def get_file_post(channel_id: int):
        async with async_session() as session:
            res = await session.execute(select(FileUserModel.title, FileUserModel.content).where(
                FileUserModel.channel_id == channel_id
            ))
            return res.first()

    async def get_news_post(self, table):
        async with async_session() as session:
            res = await session.execute(
                select(table.title, table.content, table.pictureUrl).order_by(func.random())
                .limit(1)
            )
            return res.first()
