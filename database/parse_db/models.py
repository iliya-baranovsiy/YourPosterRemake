from sqlalchemy import Date, Index, String
from sqlalchemy.orm import Mapped, mapped_column
import datetime
from database.engines import Base
from datetime import date, timedelta


class BaseStruct(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), unique=True)
    content: Mapped[str]
    pictureUrl: Mapped[str | None]
    addingDate: Mapped[datetime.date] = mapped_column(Date)
    dropDate: Mapped[datetime.date] = mapped_column(Date)

    def __init__(self, title, content, pictureUrl):
        self.title = title
        self.content = content
        self.pictureUrl = pictureUrl
        self.addingDate = date.today()
        self.dropDate = self.addingDate + timedelta(days=2)


class NewsTable(BaseStruct):
    __tablename__ = "WorldNews"
    __table_args__ = (
        Index('title_drop_index_news', 'title', 'dropDate'),
    )


class SportTable(BaseStruct):
    __tablename__ = "SportsNews"
    __table_args__ = (
        Index('title_drop_index_sports', 'title', 'dropDate'),
    )


class CryptoCurrencyTable(BaseStruct):
    __tablename__ = "CryptoCurrencyNews"
    __table_args__ = (
        Index('title_drop_index_crypto', 'title', 'dropDate'),
    )


class ItTechnologiesTable(BaseStruct):
    __tablename__ = "ItTechnologiesNews"
    __table_args__ = (
        Index('title_drop_index_IT', 'title', 'dropDate'),
    )


class AiNewsTable(BaseStruct):
    __tablename__ = "AiNews"
    __table_args__ = (
        Index('title_drop_index_AI', 'title', 'dropDate'),
    )


class ScienceTable(BaseStruct):
    __tablename__ = "ScienceNews"
    __table_args__ = (
        Index('title_drop_index_science', 'title', 'dropDate'),
    )


class ShowBisTable(BaseStruct):
    __tablename__ = "ShowBisNews"
    __table_args__ = (
        Index('title_drop_index_showbis', 'title', 'dropDate'),
    )


class GamesTable(BaseStruct):
    __tablename__ = "GamesNews"
    __table_args__ = (
        Index('title_drop_index_games', 'title', 'dropDate'),
    )
