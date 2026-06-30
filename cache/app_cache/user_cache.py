import json
from ..redis_instance import redis_engine


class UserCache:
    def __init__(self):
        self.cache_name = "user_data_cache"

    async def add_cache(self, tg_id: int,
                        username: str,
                        payment_plan: str,
                        balance: float,
                        automatic_buy: bool,
                        end_date: str | None,
                        pending_plan: str,
                        priority: int):
        async with redis_engine as redis:
            json_data = {
                "tg_id": tg_id,
                "username": username,
                "payment_plan": payment_plan,
                "balance": balance,
                "automatic_buy": automatic_buy,
                "end_date": end_date,
                "pending_plan": pending_plan,
                "priority": priority,
            }
            await redis.hset(self.cache_name, str(tg_id), json.dumps(json_data))

    async def get_cache(self, tg_id: int):
        async with redis_engine as redis:
            cache = await redis.hget(self.cache_name, str(tg_id))
            return json.loads(cache.encode()) if cache else None

    async def update_cache(self,
                           tg_id: int,
                           username: str,
                           payment_plan: str,
                           balance: float,
                           automatic_buy: bool,
                           end_date: str,
                           pending_plan: str,
                           priority: int):
        async with redis_engine as redis:
            existing_cache = await self.get_cache(tg_id)
            existing_cache["username"] = username
            existing_cache["payment_plan"] = payment_plan
            existing_cache["balance"] = balance
            existing_cache["automatic_buy"] = automatic_buy
            existing_cache["end_date"] = end_date
            existing_cache["priority"] = priority
            existing_cache["pending_plan"] = pending_plan
            await redis.hset(self.cache_name, str(tg_id), json.dumps(existing_cache))

    async def clear_cache(self):
        async with redis_engine as redis:
            await redis.delete(self.cache_name)

    async def get_only_payment_plan_cache(self, tg_id: int):
        data = await self.get_cache(tg_id=tg_id)
        return data["payment_plan"] if data else None

    async def delete_user_cache(self, user_id: int):
        async with redis_engine as redis:
            await redis.hdel(self.cache_name, str(user_id))
