from datetime import date
from business_logic.repositories.user_repository import UserRepository
from business_logic.repositories.cache_repository import UserCacheRepository
from business_logic.entities.user_entity import User


class UserService:
    def __init__(self):
        self.cache = UserCacheRepository()
        self.repo = UserRepository()

    async def create_user(self, tg_id, username):
        user_cache = await self.cache.get_user_cache(tg_id)
        if user_cache:
            return
        user_data = await self.repo.get_record(tg_id)
        if user_data:
            await self.cache.add_lost_user_cache(user_data)
            return
        username = "@" + username if username else "Undefind"
        await self.repo.create_record(tg_id, username)
        await self.cache.create_user_cache(tg_id=tg_id, username=username)

    async def get_user(self, tg_id):
        user_cache = await self.cache.get_user_cache(tg_id=tg_id)
        if user_cache:
            return user_cache
        user_data = await self.repo.get_record(tg_id=tg_id)
        if user_data:
            await self.cache.add_lost_user_cache(user_data)
            return user_data

    async def update_user(self, user: User):
        await self.repo.update(user=user, start_date=date.today())
        await self.cache.update_user_cache(user=user)
