import json
from ..redis_instance import redis_engine


class UserCache:
    def __init__(self):
        self.cache_name = "user_data_cache"

    async def add_cache(self, tg_id, username, payment_plan, balance, automatic_buy,
                        end_date, activate_date):
        async with redis_engine as redis:
            json_data = {
                "tg_id": tg_id,
                "username": username,
                "payment_plan": payment_plan,
                "balance": balance,
                "automatic_buy": automatic_buy,
                "end_date": end_date,
                "activate_date": activate_date
            }
            await redis.hset(self.cache_name, tg_id, json.dumps(json_data))

    async def get_cache(self, tg_id):
        async with redis_engine as redis:
            cache = await redis.hget(self.cache_name, tg_id)
            return json.loads(cache) if cache else None


    async def clear_cache(self):
        async with redis_engine as redis:
            await redis.delete(self.cache_name)
