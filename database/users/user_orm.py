from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select
from .models import UserModel
from ..payments.models import PaymentModel
from ..engines import async_session


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
            query = select(UserModel.username, UserModel.balance, PaymentModel).join(
                PaymentModel, UserModel.tg_id == PaymentModel.user_id
            ).where(
                UserModel.tg_id == tg_id
            )
            executing = await session.execute(query)
            result = executing.all()
            if result:
                return result[0]
            else:
                return None
