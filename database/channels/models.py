from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Index, BigInteger, Enum, text, Time
from datetime import time
from database.engines import Base
from business_logic.services.channels_service.options.options import PostTheme, Resource
from database.payments.options import PLAN_INFO, PaymentOptions


class ChannelsModel(Base):
    __tablename__ = "Channels"

    id: Mapped[int] = mapped_column(primary_key=True)
    channel_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    title: Mapped[str] = mapped_column(default="Undefined")
    owner_id: Mapped[int] = mapped_column(ForeignKey("Users.tg_id"))
    posts_count: Mapped[int] = mapped_column(default=0)

    owner: Mapped["UserModel"] = relationship("UserModel", back_populates="channels")
    channel_settings: Mapped[list["ChannelsSettingsModel"]] = relationship("ChannelsSettingsModel",
                                                                           back_populates="channel",
                                                                           passive_deletes=True)
    times: Mapped[list["PostsTimesModel"]] = relationship("PostsTimesModel",
                                                          back_populates="channel",
                                                          passive_deletes=True)

    __table_args__ = (Index("channels_index", "channel_id", "owner_id"),)


class ChannelsSettingsModel(Base):
    __tablename__ = "ChannelsSettings"

    id: Mapped[int] = mapped_column(primary_key=True)
    channel_id: Mapped[int] = mapped_column(ForeignKey("Channels.channel_id", ondelete="CASCADE"), unique=True)
    posts_available_count: Mapped[int] = mapped_column(default=PLAN_INFO[PaymentOptions.STANDART].posts_count)
    posts_count: Mapped[int] = mapped_column(default=0)
    theme: Mapped[PostTheme] = mapped_column(Enum(PostTheme),
                                             default=PostTheme.UNDEFINED,
                                             server_default=text("'UNDEFINED'"))
    is_active_posting: Mapped[bool] = mapped_column(default=False)
    resource: Mapped[Resource] = mapped_column(Enum(Resource),
                                               default=Resource.DATABASE,
                                               server_default=text("'DATABASE'"))

    channel: Mapped["ChannelsModel"] = relationship("ChannelsModel", back_populates="channel_settings")


class PostsTimesModel(Base):
    __tablename__ = "PostsTimes"

    id: Mapped[int] = mapped_column(primary_key=True)
    channel_id: Mapped[int] = mapped_column(ForeignKey("Channels.channel_id", ondelete="CASCADE"))
    time: Mapped[time] = mapped_column(Time)

    channel: Mapped["ChannelsModel"] = relationship("ChannelsModel", back_populates="times")
