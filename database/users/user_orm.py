from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, update
from decimal import Decimal
from datetime import date
from .models import UserModel
from ..payments.models import PaymentModel
from ..payments.options import PaymentOptions
from ..engines import async_session
from .user_dto import UserDto, OnlyPaymentPlanDto


class UserOrm:
    @staticmethod
    async def create_user(tg_id, username):
        async with async_session() as session:
            insert_user = insert(UserModel).values(tg_id=tg_id, username=username)
            unique_user = insert_user.on_conflict_do_nothing(index_elements=['tg_id'])
            payment = insert(PaymentModel).values(user_id=tg_id).on_conflict_do_nothing(index_elements=['user_id'])
            async with session.begin():
                await session.execute(unique_user)
                await session.execute(payment)

    @staticmethod
    async def get_user(tg_id):
        async with async_session() as session:
            query = select(UserModel.username, UserModel.balance, PaymentModel.payment_plan, PaymentModel.automatic_buy,
                           PaymentModel.end_date, PaymentModel.priority, PaymentModel.pending_plan).join(
                PaymentModel, UserModel.tg_id == PaymentModel.user_id
            ).where(
                UserModel.tg_id == tg_id
            )
            executing = await session.execute(query)
            result = executing.all()
            if result:
                result = result[0]
                return UserDto(username=result[0], balance=result[1], payment_plan=result[2], automatic_buy=result[3],
                               end_date=result[4], priority=result[5], pending_plan=result[6])
            else:
                return None

    @staticmethod
    async def update_user_data(tg_id: int, balance: Decimal, payment_plan: PaymentOptions, automatic_buy: bool,
                               pending_plan: PaymentOptions, priority: int, activate_date: date,
                               end_date: date):
        async with async_session() as session:
            payment_stmt = update(PaymentModel).values(
                payment_plan=payment_plan,
                automatic_buy=automatic_buy,
                pending_plan=pending_plan,
                priority=priority,
                activate_date=activate_date,
                end_date=end_date
            ).where(PaymentModel.user_id == tg_id)
            user_stmt = update(UserModel).values(
                balance=balance
            ).where(UserModel.tg_id == tg_id)
            async with session.begin():
                await session.execute(user_stmt)
                await session.execute(payment_stmt)
