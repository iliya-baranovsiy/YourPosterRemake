from database.extension_db.orm import ExtensionOrm
from database.extension_db.models import FileUserModel


class ExtensionFileRepository:
    def __init__(self):
        self.orm = ExtensionOrm()

    async def add_file_records(self, records: list[dict]):
        await self.orm.add_records(records=records, table=FileUserModel)

    async def delete_file_records(self, channel_id):
        await self.orm.delete_records(table=FileUserModel, channel_id=channel_id)

    async def get_file_posts_count(self, channel_id: int):
        count = await self.orm.get_records_count(channel_id=channel_id, table=FileUserModel)
        return count
