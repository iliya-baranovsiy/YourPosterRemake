from datetime import date
from business_logic.repositories.user_repository import UserRepository
from business_logic.repositories.user_cache_repository import UserCacheRepository
from business_logic.entities.user_entity import User
from database.payments.options import PaymentOptions


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

    async def get_only_payment_plan(self, tg_id) -> PaymentOptions:
        data_in_cache = await self.cache.get_only_payment_plan_cache(tg_id=tg_id)
        if data_in_cache:
            return data_in_cache
        user = await self.get_user(tg_id=tg_id)
        if user:
            await self.cache.add_lost_user_cache(user)
            return user.subscription.payment_plan
