from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from database.engines import Base


class FileUserModel(Base):
    __tablename__ = "file_user_storage"
    id: Mapped[int] = mapped_column(primary_key=True)
    channel_id: Mapped[int] = mapped_column(ForeignKey("Channels.channel_id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(200), unique=True)
    content: Mapped[str] = mapped_column(String(3600))
    channel: Mapped["ChannelsModel"] = relationship("ChannelsModel", back_populates="file_storage")


class GenerateUserModel(Base):
    __tablename__ = "generate_user_storage"
    id: Mapped[int] = mapped_column(primary_key=True)
    channel_id: Mapped[int] = mapped_column(ForeignKey("Channels.channel_id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(50), unique=True)
    content: Mapped[str] = mapped_column(String(3600))
    channel: Mapped["ChannelsModel"] = relationship("ChannelsModel", back_populates="generative_storage")
