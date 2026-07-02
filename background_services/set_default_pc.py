from cache.app_cache.channels_cache import ChannelsCache
from database.backgroundt_tasks_db.orm import BackGroundTasksORM


class DefaultPostsCountValue:
    def __init__(self):
        self.orm = BackGroundTasksORM()
        self.cache = ChannelsCache()

    async def set_default(self):
        await self.orm.set_default_posts_count()
        await self.cache.set_default_posts_count()
