from business_logic.entities.user_entity import User
from business_logic.repositories.user_repository import UserRepository
from cache.app_cache.user_cache import UserCache


class UserService:
    def __init__(self):
        self.cache = UserCache()
        self.repo = UserRepository()

    async def create_user(self, tg_id, username):
        user_cache = await self.cache.get_cache(tg_id)
        if user_cache:
            return
        user_data = await self.repo.get_record(tg_id)
        if user_data:
            return
        username = "@" + username if username else "Undefind"
        await self.repo.create_record(tg_id, username)
        await self.cache.add_cache(tg_id=tg_id, username=username)
