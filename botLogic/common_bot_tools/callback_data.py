from aiogram.filters.callback_data import CallbackData


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
