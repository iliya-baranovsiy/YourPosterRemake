from decimal import Decimal
from datetime import datetime
from cache.app_cache.user_cache import UserCache
from ..entities.user_entity import User
from ..entities.payment_plan_entity import Subscription
from database.payments.options import PaymentOptions


class UserCacheRepository:
    def __init__(self):
        self.cache = UserCache()

    async def create_user_cache(self, tg_id, username="Undefind", payment_plan="STANDART", balance=0.0,
                                automatic_buy=False,
                                end_date=None, priority=0, pending_plan="STANDART"):
        await self.cache.add_cache(tg_id=tg_id, username=username, payment_plan=payment_plan, balance=balance,
                                   automatic_buy=automatic_buy,
                                   end_date=end_date, priority=priority, pending_plan=pending_plan)

    async def get_user_cache(self, tg_id):
        cache_data = await self.cache.get_cache(tg_id=tg_id)
        if cache_data:
            return User(tg_id=tg_id, username=cache_data["username"],
                        balance=Decimal(cache_data["balance"]).quantize(Decimal("0.00")),
                        automatic_buy=cache_data["automatic_buy"],
                        subscription=Subscription(payment_plan=PaymentOptions(cache_data["payment_plan"]),
                                                  end_date_row=cache_data["end_date"],
                                                  priority=cache_data["priority"],
                                                  pending_plan=PaymentOptions(cache_data["pending_plan"]))
                        )
        return None

    async def update_user_cache(self, user: User):
        await self.cache.update_cache(user)

    async def add_lost_user_cache(self, user: User):
        await self.create_user_cache(tg_id=user.tg_id, username=user.username,
                                     payment_plan=user.subscription.payment_plan_str,
                                     balance=user.balance, automatic_buy=user.automatic_buy,
                                     end_date=user.subscription.end_date, pending_plan=user.subscription.pending_plan,
                                     priority=user.subscription.priority)
