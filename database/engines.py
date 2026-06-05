from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import  sessionmaker, DeclarativeBase
from config.configurations import settings

sync_engine = create_engine(
    url=settings.get_sync_db_url,
    echo=True,
    pool_size=100,
    max_overflow=50
)

async_engine = create_async_engine(
    url=settings.get_async_db_url,
    echo=True,
    pool_size=100,
    max_overflow=50
)


class Base(DeclarativeBase):
    pass


sync_session = sessionmaker(sync_engine)
async_session = async_sessionmaker(async_engine)
metadata_obj = Base.metadata
