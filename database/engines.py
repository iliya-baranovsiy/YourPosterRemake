from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from config.configurations import settings

sync_engine = create_engine(
    url=settings.get_sync_db_url,
    echo=True,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=300,
)

async_engine = create_async_engine(
    url=settings.get_async_db_url,
    echo=True,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=300,
    connect_args={
        "statement_cache_size": 0
    }
)


class Base(DeclarativeBase):
    pass


sync_session = sessionmaker(sync_engine)
async_session = async_sessionmaker(async_engine)
metadata_obj = Base.metadata
