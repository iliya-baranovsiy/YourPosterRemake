from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from botLogic.common_bot_tools.callback_data import ChannelSettingsCb, LoadCb
from business_logic.common_options.status_option import Status


class KbBuilder:
    def __init__(self, channel_id: int):
        self.kb = []
        self.channel_id = channel_id

    def create_load_button(self):
        self.kb.append(
            [InlineKeyboardButton(text="📤 Загрузить файл",
                                  callback_data=LoadCb(channel_id=self.channel_id, action="load").pack())]
        )

    def create_request_to_del_button(self):
        self.kb.append(
            [InlineKeyboardButton(text="🗑️ Удалить публикации",
                                  callback_data=LoadCb(channel_id=self.channel_id, action="requestToDel").pack())]
        )

    def create_back_button(self):
        self.kb.append(
            [InlineKeyboardButton(
                text="◀️ Назад", callback_data=ChannelSettingsCb(
                    channel_id=self.channel_id,
                    action="openMenu", ).pack()
            )]
        )

    def create_request_to_del_buttons(self):
        self.kb.append(
            [
                InlineKeyboardButton(text="✅ Удалить",
                                     callback_data=LoadCb(channel_id=self.channel_id, action="delete").pack()),
                InlineKeyboardButton(text="❌ Отмена", callback_data=ChannelSettingsCb(
                    action="loadFileMenu",
                    channel_id=self.channel_id, ).pack())
            ]
        )


class LoadFileKb:
    def __init__(self, channel_id: int, status: Status, file_posts_count):
        self.channel_id = channel_id
        self.builder = KbBuilder(channel_id=self.channel_id)
        self.status = status
        self.count = file_posts_count

    def get_kb(self):
        if self.status == Status.OK:
            self.builder.create_load_button()
        if self.count > 0:
            self.builder.create_request_to_del_button()
        self.builder.create_back_button()
        return InlineKeyboardMarkup(inline_keyboard=self.builder.kb)


def get_request_to_del_kb(channel_id: int):
    builder = KbBuilder(channel_id=channel_id)
    builder.create_request_to_del_buttons()
    return InlineKeyboardMarkup(inline_keyboard=builder.kb)
