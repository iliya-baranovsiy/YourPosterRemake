from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, func, delete

from database.engines import async_session


class ExtensionOrm:

    @staticmethod
    async def add_records(records: list[dict], table):
        stmt = insert(table).values(records)
        unique_stmt = stmt.on_conflict_do_nothing(index_elements=["title"])
        async with async_session() as session:
            await session.execute(unique_stmt)
            await session.commit()

    @staticmethod
    async def get_records_count(channel_id: int, table):
        stmt = select(func.count()).select_from(table).where(table.channel_id == channel_id)
        async with async_session() as session:
            count = await session.scalar(stmt)
        return count

    @staticmethod
    async def delete_records(channel_id: int, table):
        async with async_session() as session:
            await session.execute(
                delete(table).where(table.channel_id == channel_id)
            )
            await session.commit()
