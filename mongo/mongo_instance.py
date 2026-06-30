from motor.motor_asyncio import AsyncIOMotorClient
from config.configurations import settings

client = AsyncIOMotorClient(settings.get_mongo_url)



