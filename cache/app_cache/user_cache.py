import json
from ..redis_instance import redis_engine
from business_logic.entities.user_entity import User


class UserCache:
    def __init__(self):
        self.cache_name = "user_data_cache"

    async def add_cache(self, tg_id, username, payment_plan, balance, automatic_buy,
                        end_date):
        async with redis_engine as redis:
            json_data = {
                "tg_id": tg_id,
                "username": username,
                "payment_plan": payment_plan,
                "balance": float(balance),
                "automatic_buy": automatic_buy,
                "end_date": end_date,
            }
            await redis.hset(self.cache_name, tg_id, json.dumps(json_data))

    async def get_cache(self, tg_id):
        async with redis_engine as redis:
            cache = await redis.hget(self.cache_name, tg_id)
            return json.loads(cache) if cache else None

    async def update_cache(self, user: User):
        async with redis_engine as redis:
            existing_cache = await self.get_cache(user.tg_id)
            print(existing_cache)
            existing_cache["username"] = user.username
            existing_cache["payment_plan"] = user.payment_plan_str
            existing_cache["balance"] = float(user.balance)
            existing_cache["automatic_buy"] = user.automatic_buy
            existing_cache["end_date"] = user.end_date
            await redis.hset(self.cache_name, user.tg_id, json.dumps(existing_cache))

    async def clear_cache(self):
        async with redis_engine as redis:
            await redis.delete(self.cache_name)
