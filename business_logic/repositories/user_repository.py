from .base_repository import BaseRepository
from business_logic.entities.user_entity import User
from database.users.user_orm import UserOrm


class UserRepository(BaseRepository):
    def __init__(self, user: User):
        self.user = user
        self.orm = UserOrm()

    async def create_record(self):
        await self.orm.create_user(self.user)

    async def get_record(self):
        pass
