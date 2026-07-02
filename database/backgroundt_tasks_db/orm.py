from datetime import date
from sqlalchemy import select, update

from ..engines import async_session
from ..payments.models import PaymentModel
from database.channels.models import ChannelsSettingsModel


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
