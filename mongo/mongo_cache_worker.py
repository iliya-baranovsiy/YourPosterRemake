from .mongo_instance import client
import asyncio


class MongoExceptionWork:
    def __init__(self):
        self.db = client["exception_db"]
        self.mongo = self.db["exception_ids"]

    async def create_index(self):
        await self.mongo.create_index("id", unique=True)

    async def write_id(self, id_: int):
        await self.mongo.update_one(
            {"id": id_},
            {"$setOnInsert": {"id": id_}},
            upsert=True
        )

    async def get_all_ids(self):
        return [doc["id"] async for doc in self.mongo.find({}, {"_id": 0, "id": 1})]

    async def delete_id(self, id_: int):
        await self.mongo.delete_one({"id": id_})
