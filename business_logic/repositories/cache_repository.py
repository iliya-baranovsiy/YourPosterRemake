from cache.app_cache.user_cache import UserCache
from ..entities.user_entity import User
from database.payments.options import PaymentOptions


class UserCacheRepository:
    def __init__(self):
        self.cache = UserCache()

    async def create_user_cache(self, tg_id, username="Undefind", payment_plan="STANDART", balance=0.0,
                                automatic_buy=False,
                                end_date=None):
        await self.cache.add_cache(tg_id=tg_id, username=username, payment_plan=payment_plan, balance=balance,
                                   automatic_buy=automatic_buy,
                                   end_date=end_date)

    async def get_user_cache(self, tg_id):
        cache_data = await self.cache.get_cache(tg_id=tg_id)
        if cache_data:
            return User(tg_id=tg_id, username=cache_data["username"], balance=cache_data["balance"],
                        payment_plan=PaymentOptions(cache_data["payment_plan"]),
                        automatic_buy=cache_data["automatic_buy"],
                        end_date_row=cache_data["end_date"])
        return None

    async def update_user_cache(self, user: User):
        await self.cache.update_cache(user)

    async def add_lost_user_cache(self, user: User):
        await self.create_user_cache(tg_id=user.tg_id, username=user.username, payment_plan=user.payment_plan_str,
                                     balance=user.balance, automatic_buy=user.automatic_buy, end_date=user.end_date)
