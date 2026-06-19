from ..redis_instance import redis_engine


class ChannelsCache:
    def __init__(self):
        self.channels_namespace = "user_channels"
        self.channels_settings_namespace = "channel_settings"

    async def get_user_channels(self, owner_id: int):
        async with redis_engine as redis:
            data = await redis.hgetall(f"{self.channels_namespace}:{owner_id}")
            return data if data else None

    async def add_channel(self,
                          channel_id: int,
                          channel_name: str,
                          owner_id: int):
        async with redis_engine as redis:
            await redis.hset(f"{self.channels_namespace}:{owner_id}", channel_id, channel_name)

