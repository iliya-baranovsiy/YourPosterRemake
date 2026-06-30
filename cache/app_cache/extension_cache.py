import json
from ..redis_instance import redis_engine
from business_logic.entities.channel_entity import Resource


class ExtensionCache:
    def __init__(self, type_: Resource = Resource.FILE):
        self.namespace = "file_extension" if type_ == Resource.FILE else "generate_extension"

    async def add_count(self, channel_id: int, count: int):
        data = {
            "records_count": count
        }
        async with redis_engine as redis:
            await redis.hset(self.namespace, str(channel_id), json.dumps(data))

    async def get_count(self, channel_id: int):
        async with redis_engine as redis:
            row_data = await redis.hget(self.namespace, str(channel_id))
            return json.loads(row_data) if row_data else None

    async def delete_posts_count(self, channel_id: int):
        async with redis_engine as redis:
            await redis.hdel(self.namespace, str(channel_id))

    async def clear_count(self):
        async with redis_engine as redis:
            await redis.delete("file_extension")
            await redis.delete("generate_extension")
