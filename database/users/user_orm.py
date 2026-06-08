from sqlalchemy.dialects.postgresql import insert
from .models import UserModel
from ..payments.models import PaymentModel
from ..engines import async_session
from business_logic.entities.user_entity import User


class UserOrm:
    @staticmethod
    async def create_user(user: User):
        async with async_session() as session:
            insert_user = insert(UserModel).values(tg_id=user.tg_id, username=user.username)
            unique_user = insert_user.on_conflict_do_nothing(index_elements=['tg_id'])
            payment = insert(PaymentModel).values(user_id=user.tg_id).on_conflict_do_nothing(index_elements=['user_id'])
            async with session.begin():
                await session.execute(unique_user)
                await session.execute(payment)
