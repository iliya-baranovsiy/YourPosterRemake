from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from business_logic.entities.channel_entity import UserChannelsInfo
from botLogic.common_bot_tools.callback_data import ChannelCb


class MenuKbBuilder:
    def __init__(self):
        self.kb_buttons = []

    def create_channel_button(self, channel_name: str, channel_id: int):
        self.kb_buttons.append([InlineKeyboardButton(text=channel_name,
                                                     callback_data=ChannelCb(
                                                         channel_id=channel_id,
                                                         action="openChannelMenu",
                                                     ).pack())])

    def create_add_channel_button(self):
        self.kb_buttons.append([InlineKeyboardButton(text="➕ Добавить канал",
                                                     callback_data=ChannelCb(
                                                         channel_id=0,
                                                         action="addChannel",
                                                     ).pack())])

    def create_back_button(self):
        self.kb_buttons.append([InlineKeyboardButton(text="◀️ Назад", callback_data="autoposting_menu")])


class MenuKb:
    def __init__(self, data: UserChannelsInfo):
        self.available_count = data.channels_available_count - data.channels_count
        self.channels_count = data.channels_count
        self.channels_list = data.channels
        self.builder = MenuKbBuilder()

    def create_kb(self):
        if self.channels_count != 0:
            for i in self.channels_list:
                self.builder.create_channel_button(channel_name=i.channel_name, channel_id=i.channel_id)
        if self.available_count > 0:
            self.builder.create_add_channel_button()
        self.builder.create_back_button()
        return InlineKeyboardMarkup(inline_keyboard=self.builder.kb_buttons)
