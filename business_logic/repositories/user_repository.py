from database.users.user_orm import UserOrm


class UserRepository:
    def __init__(self):
        self.orm = UserOrm()

    async def create_record(self, tg_id, username):
        await self.orm.create_user(tg_id, username)

    async def get_record(self, tg_id):
        await self.orm.get_user(tg_id)
