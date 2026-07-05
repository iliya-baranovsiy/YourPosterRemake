from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, exists

from .models import PaymentTransactions
from .options import PaymentStatus
from database.engines import async_session


class PaymentDataORM:

    async def insert_pyment(self, user_id: int, amount: int, telegram_charge_id: str, payload: str,
                            status: PaymentStatus):
        stmt = insert(PaymentTransactions).values(
            user_id=user_id,
            amount=amount,
            telegram_charge_id=telegram_charge_id,
            payload=payload,
            status=status,
        )
        unique_stmt = stmt.on_conflict_do_nothing(index_elements=["telegram_charge_id"])
        async with async_session() as session:
            await session.execute(unique_stmt)
            await session.commit()

    async def get_payment_data(self, user_id: int, telegram_charge_id: str):
        async with async_session() as session:
            stmt = select(PaymentTransactions.status).where(
                PaymentTransactions.user_id == user_id,
                PaymentTransactions.telegram_charge_id == telegram_charge_id
            )
            res = await session.execute(stmt)
            return res.scalars().first()

    async def check_existing_payment_data(self, telegram_charge_id: str):
        async with async_session() as session:
            stmt = select(
                exists().where(PaymentTransactions.telegram_charge_id == telegram_charge_id)
            )
            res = await session.execute(stmt)
            return res.scalar()
