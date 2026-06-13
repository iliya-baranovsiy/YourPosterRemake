from database.users.user_orm import UserOrm
from ..entities.user_entity import User


class UserRepository:
    def __init__(self):
        self.orm = UserOrm()

    async def create_record(self, tg_id, username):
        await self.orm.create_user(tg_id, username)

    async def get_record(self, tg_id):
        user_data = await self.orm.get_user(tg_id)
        if user_data:
            return User(tg_id=tg_id, username=user_data[0], balance=user_data[1], payment_plan=user_data[2],
                        automatic_buy=user_data[3], end_date_row=user_data[4])
        return None
