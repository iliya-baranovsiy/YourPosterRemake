from database.users.user_orm import UserOrm
from ..entities.user_entity import User
from ..entities.payment_plan_entity import Subscription


class UserRepository:
    def __init__(self):
        self.orm = UserOrm()

    async def create_record(self, tg_id, username):
        await self.orm.create_user(tg_id, username)

    async def get_record(self, tg_id):
        user_data = await self.orm.get_user(tg_id)
        if user_data:
            return User(tg_id=tg_id, username=user_data.username, balance=user_data.balance,
                        automatic_buy=user_data.automatic_buy,
                        subscription=Subscription(payment_plan=user_data.payment_plan, end_date_row=user_data.end_date,
                                                  priority=user_data.priority, pending_plan=user_data.priority)
                        )
        return None
