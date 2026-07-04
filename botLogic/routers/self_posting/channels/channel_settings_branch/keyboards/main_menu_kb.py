from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from botLogic.common_bot_tools.callback_data import ChannelSettingsCb, ChannelCb


class KeyboardBuilder:
    def __init__(self):
        self.kb = []

    def create_make_post_button(self):
        self.kb.append([InlineKeyboardButton(text="Сделать пост", callback_data="make_post")])

    def create_settings_button(self, channel_id: int):
        self.kb.append([InlineKeyboardButton(text="⚙️ Настройки постинга",
                                             callback_data=ChannelSettingsCb(
                                                 channel_id=channel_id,
                                                 action="openMenu", ).pack())])

    def create_delete_button(self, channel_id: int):
        self.kb.append(
            [InlineKeyboardButton(text="🗑️ Отвязать канал",
                                  callback_data=ChannelCb(
                                      channel_id=channel_id,
                                      action="requestToDrop"
                                  ).pack())])

    def create_back_button(self):
        self.kb.append([InlineKeyboardButton(text="◀️ Назад", callback_data="channels")])


class MenuKb:
    def __init__(self, channel_id: int):
        self.channel_id = channel_id
        self.builder = KeyboardBuilder()

    def get_kb(self):
        self.builder.create_settings_button(channel_id=self.channel_id)
        self.builder.create_delete_button(channel_id=self.channel_id)
        self.builder.create_back_button()
        return InlineKeyboardMarkup(inline_keyboard=self.builder.kb)
