import json
from ..redis_instance import redis_engine
from business_logic.entities.user_entity import User


class UserCache:
    def __init__(self):
        self.cache_name = "user_data_cache"

    async def add_cache(self, tg_id, username, payment_plan, balance, automatic_buy,
                        end_date, pending_plan, priority):
        async with redis_engine as redis:
            json_data = {
                "tg_id": tg_id,
                "username": username,
                "payment_plan": payment_plan,
                "balance": float(balance),
                "automatic_buy": automatic_buy,
                "end_date": end_date,
                "pending_plan": pending_plan,
                "priority": priority,
            }
            await redis.hset(self.cache_name, tg_id, json.dumps(json_data))

    async def get_cache(self, tg_id):
        async with redis_engine as redis:
            cache = await redis.hget(self.cache_name, tg_id)
            return json.loads(cache) if cache else None

    async def update_cache(self, user: User):
        async with redis_engine as redis:
            existing_cache = await self.get_cache(user.tg_id)
            existing_cache["username"] = user.username
            existing_cache["payment_plan"] = user.subscription.payment_plan_str
            existing_cache["balance"] = float(user.balance)
            existing_cache["automatic_buy"] = user.automatic_buy
            existing_cache["end_date"] = user.subscription.end_date
            existing_cache["priority"] = user.subscription.priority
            existing_cache["pending_plan"] = user.subscription.pending_plan
            await redis.hset(self.cache_name, user.tg_id, json.dumps(existing_cache))

    async def clear_cache(self):
        async with redis_engine as redis:
            await redis.delete(self.cache_name)
