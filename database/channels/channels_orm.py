import asyncio
from sqlalchemy import select, delete, exists, update
from sqlalchemy.dialects.postgresql import insert
from .models import ChannelsModel, ChannelsSettingsModel, PostsTimesModel
from ..engines import async_session
from .schemas import ChannelSettingsDto
from business_logic.services.channels_service.options.options import PostTheme, Resource
from .times_functinon import to_delete, to_insert


class ChannelsOrm:

    @staticmethod
    async def get_user_channels(tg_id: int):
        async with async_session() as session:
            query = select(ChannelsModel.channel_id, ChannelsModel.title).where(ChannelsModel.owner_id == tg_id)
            executing = await session.execute(query)
            result = executing.all()
            return result if result else None

    @staticmethod
    async def get_channel_settings(channel_id: int):
        async with async_session() as session:
            query = (
                select(
                    ChannelsModel.title,
                    ChannelsSettingsModel.posts_count,
                    ChannelsSettingsModel.posts_available_count,
                    ChannelsSettingsModel.theme,
                    ChannelsSettingsModel.resource,
                    ChannelsSettingsModel.is_active_posting,
                )
                .select_from(ChannelsModel)
                .join(
                    ChannelsSettingsModel,
                    ChannelsSettingsModel.channel_id == ChannelsModel.channel_id
                )
                .where(ChannelsModel.channel_id == channel_id)
            )
            channels_times_query = select(PostsTimesModel.time).where(PostsTimesModel.channel_id == channel_id)

            query_executing = await session.execute(query)
            times_executing = await session.execute(channels_times_query)

            query_result = query_executing.first()
            times_result = times_executing.all()

            dto_result = ChannelSettingsDto(post_count=query_result[1],
                                            post_available_count=query_result[2],
                                            post_theme=query_result[3],
                                            posts_resource=query_result[4],
                                            is_active_posting=query_result[5],
                                            channel_name=query_result[0],
                                            posts_times=[i[0] for i in times_result]
                                            )
            return dto_result

    @staticmethod
    async def check_channel_existing(channel_id: int):
        async with async_session() as session:
            stmt = select(
                exists().where(ChannelsModel.channel_id == channel_id)
            )
            result = await session.execute(stmt)
            return result.scalar()

    @staticmethod
    async def add_channel(channel_id: int,
                          channel_title: str,
                          owner_id: int):
        async with async_session() as session:
            insert_channel = insert(ChannelsModel).values(
                channel_id=channel_id,
                title=channel_title,
                owner_id=owner_id,
            )
            insert_channel_settings = insert(ChannelsSettingsModel).values(
                channel_id=channel_id
            )
            unique_insert_channel_settings = insert_channel_settings.on_conflict_do_nothing(
                index_elements=["channel_id"])
            unique_channel = insert_channel.on_conflict_do_nothing(index_elements=["channel_id"])
            async with session.begin():
                await session.execute(unique_channel)
                await session.execute(unique_insert_channel_settings)

    @staticmethod
    async def delete_channel(channel_id: int):
        async with async_session() as session:
            await session.execute(
                delete(ChannelsModel).where(ChannelsModel.channel_id == channel_id)
            )
            await session.commit()

    @staticmethod
    async def update_channel_settings(channel_id: int, posts_available_count: int, posts_count: int, theme: PostTheme,
                                      is_active_posting: bool, resource: Resource):
        async with async_session() as session:
            stmt = update(ChannelsSettingsModel).values(
                posts_available_count=posts_available_count,
                posts_count=posts_count,
                theme=theme,
                is_active_posting=is_active_posting,
                resource=resource
            ).where(ChannelsSettingsModel.channel_id == channel_id)
            async with session.begin():
                await session.execute(stmt)

    async def update_channel_times(self, channel_id: int, times: list):
        async with async_session() as session:
            db_data = await self._get_only_channel_times(channel_id=channel_id)
            to_del = list(to_delete(db_data=db_data, entity_data=times))
            to_ins = list(to_insert(db_data=db_data, entity_data=times))
            async with session.begin():
                if to_del:
                    await session.execute(
                        delete(PostsTimesModel).where(
                            PostsTimesModel.channel_id == channel_id,
                            PostsTimesModel.time.in_(to_del)
                        )
                    )
                if to_ins:
                    await session.execute(
                        insert(PostsTimesModel).values(
                            channel_id=channel_id,
                            time=to_ins[0]
                        )
                    )

    async def _get_only_channel_times(self, channel_id: int) -> list:
        async with async_session() as session:
            query = select(PostsTimesModel.time).where(PostsTimesModel.channel_id == channel_id)
            executing = await session.execute(query)
            result = executing.all()
            if result:
                return [i[0] for i in result]
            return []
