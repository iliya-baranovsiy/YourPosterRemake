from decimal import Decimal
from datetime import datetime
from cache.app_cache.user_cache import UserCache
from ..entities.user_entity import User
from ..entities.payment_plan_entity import Subscription
from database.payments.options import PaymentOptions
from mongo.mongo_cache_worker import MongoExceptionWork
from events.redis_exeption_event import redis_exception


class UserCacheRepository:
    def __init__(self):
        self.cache = UserCache()
        self.mongo = MongoExceptionWork()

    async def create_user_cache(self, tg_id: int,
                                username: str = "Undefind",
                                payment_plan: str = PaymentOptions.STANDART.value,
                                balance: float = 0.0,
                                automatic_buy: bool = False,
                                end_date: str | None = None, priority: int = 0,
                                pending_plan: str = PaymentOptions.STANDART.value):
        try:
            await self.cache.add_cache(tg_id=tg_id,
                                       username=username,
                                       payment_plan=payment_plan,
                                       balance=balance,
                                       automatic_buy=automatic_buy,
                                       end_date=end_date,
                                       priority=priority,
                                       pending_plan=pending_plan)
        except:
            await self.mongo.write_id(id_=tg_id)
            redis_exception.set()

    async def get_user_cache(self, tg_id: int):
        try:
            cache_data = await self.cache.get_cache(tg_id=tg_id)
            if cache_data:
                return User(tg_id=tg_id,
                            username=cache_data["username"],
                            balance=Decimal(cache_data["balance"]).quantize(Decimal("0.00")),
                            automatic_buy=cache_data["automatic_buy"],
                            subscription=Subscription(
                                payment_plan=PaymentOptions(cache_data["payment_plan"]),
                                end_date_row=datetime.strptime(cache_data["end_date"], "%Y-%m-%d").date() if cache_data[
                                    "end_date"] else None,
                                priority=cache_data["priority"],
                                pending_plan=PaymentOptions(cache_data["pending_plan"]))
                            )
            return None
        except:
            await self.mongo.write_id(id_=tg_id)
            redis_exception.set()
            return None

    async def update_user_cache(self, user: User):
        try:
            await self.cache.update_cache(tg_id=user.tg_id,
                                          username=user.username,
                                          balance=float(user.balance),
                                          payment_plan=user.subscription.payment_plan_str,
                                          pending_plan=user.subscription.pending_plan.value,
                                          automatic_buy=user.automatic_buy,
                                          priority=user.subscription.priority,
                                          end_date=str(
                                              user.subscription.end_date_row) if user.subscription.end_date_row else None
                                          )
        except:
            await self.mongo.write_id(id_=user.tg_id)
            redis_exception.set()

    async def add_lost_user_cache(self, user: User):
        try:
            await self.create_user_cache(tg_id=user.tg_id,
                                         username=user.username,
                                         payment_plan=user.subscription.payment_plan_str,
                                         balance=float(user.balance),
                                         automatic_buy=user.automatic_buy,
                                         end_date=str(
                                             user.subscription.end_date_row) if user.subscription.end_date_row else None,
                                         pending_plan=user.subscription.pending_plan.value,
                                         priority=user.subscription.priority)
        except:
            await self.mongo.write_id(id_=user.tg_id)
            redis_exception.set()

    async def get_only_payment_plan_cache(self, tg_id: int):
        try:
            cache_data = await self.cache.get_only_payment_plan_cache(tg_id=tg_id)
            return PaymentOptions(cache_data) if cache_data else None
        except:
            await self.mongo.write_id(id_=tg_id)
            redis_exception.set()
            return None

    async def delete_user_cache(self, user_id: int):
        try:
            await self.cache.delete_user_cache(user_id=user_id)
        except:
            await self.mongo.write_id(id_=user_id)
            redis_exception.set()
