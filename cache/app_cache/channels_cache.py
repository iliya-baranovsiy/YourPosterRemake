import json
from ..redis_instance import redis_engine


class ChannelsCache:
    def __init__(self):
        self.channels_namespace = "user_channels"
        self.channels_settings_namespace = "channel_settings"

    async def add_channel(self,
                          channel_id: int,
                          owner_id: int,
                          channel_name: str,
                          posts_available_count: int,
                          posts_count: int,
                          theme: str,
                          time: list,
                          posting_is_active: bool,
                          resource: str):
        data = {
            "channel_name": channel_name,
            "posts_available_count": posts_available_count,
            "posts_count": posts_count,
            "theme": theme,
            "time": time,
            "posting_is_active": posting_is_active,
            "resource": resource
        }
        async with redis_engine as redis:
            await redis.hset(f"{self.channels_namespace}:{owner_id}", channel_id, channel_name)
            await redis.hset(self.channels_settings_namespace, str(channel_id), json.dumps(data))

    async def get_user_channels(self, owner_id: int):
        async with redis_engine as redis:
            data = await redis.hgetall(f"{self.channels_namespace}:{owner_id}")
            return data if data else None

    async def get_channel_settings(self, channel_id: int):
        async with redis_engine as redis:
            cache = await redis.hget(self.channels_settings_namespace, str(channel_id))
            return json.loads(cache) if cache else None

    async def drop_channel(self, channel_id: int, owner_id: int):
        async with redis_engine as redis:
            await redis.hdel(f"{self.channels_namespace}:{owner_id}", channel_id)
            await redis.hdel(self.channels_settings_namespace, str(channel_id))

    async def clear_channels_cache(self):
        async with redis_engine as redis:
            await redis.delete(self.channels_settings_namespace)
            cursor = 0

            while True:
                cursor, keys = await redis.scan(
                    cursor=cursor,
                    match=f"{self.channels_namespace}:*"
                )

                if keys:
                    await redis.delete(*keys)

                if cursor == 0:
                    break
