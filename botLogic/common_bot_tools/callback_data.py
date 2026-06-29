from aiogram.filters.callback_data import CallbackData
from business_logic.entities.channel_entity import Resource


class ChannelSettingsCb(CallbackData, prefix="Settings"):
    action: str
    channel_id: int


class ThemeCb(CallbackData, prefix="SetTheme"):
    action: str
    channel_id: int
    theme: str


class TimeCb(CallbackData, prefix="Times"):
    action: str
    channel_id: int
    time_: str


class ChannelCb(CallbackData, prefix="Channel"):
    channel_id: int
    action: str


class ResourceCb(CallbackData, prefix="Resource"):
    channel_id: int
    resource: Resource
    action: str


class LoadCb(CallbackData, prefix="fileLoad"):
    channel_id: int
    action: str
