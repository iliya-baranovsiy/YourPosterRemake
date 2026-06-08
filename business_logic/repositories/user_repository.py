from .base_repository import BaseRepository
from business_logic.entities.user_entity import User
from database.users.user_orm import UserOrm
from cache.app_cache.user_cache import user_cache


class UserRepository(BaseRepository):
    def __init__(self, user: User):
        self.user = user
        self.orm = UserOrm()

    async def create_record(self):
        user_data_cache = await user_cache.get_cache(self.user.tg_id)
        if user_data_cache:
            return
        await self.orm.create_user(self.user)
        await user_cache.add_cache(tg_id=self.user.tg_id, username=self.user.username)
