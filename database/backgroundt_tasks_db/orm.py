from datetime import date
from sqlalchemy import select

from ..engines import async_session
from ..payments.models import PaymentModel


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
