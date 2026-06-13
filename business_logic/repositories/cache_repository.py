from cache.app_cache.user_cache import UserCache


class UserCacheRepository:
    def __init__(self):
        self.cache = UserCache()

    async def add_user_cache(self, tg_id, username="Undefind", payment_plan="STANDART", balance=0, automatic_buy=False,
                             end_date=None, activate_date=None):
        await self.cache.add_cache(tg_id=tg_id, username=username, payment_plan=payment_plan, balance=balance,
                                   automatic_buy=automatic_buy,
                                   end_date=end_date, activate_date=activate_date)

    async def get_user_cache(self, tg_id):
        cache_data = await self.cache.get_cache(tg_id=tg_id)
        return cache_data
