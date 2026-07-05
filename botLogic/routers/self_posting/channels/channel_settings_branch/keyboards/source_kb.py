from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from business_logic.entities.channel_entity import ChannelSettings, Resource
from database.payments.options import PaymentOptions
from botLogic.common_bot_tools.callback_data import ChannelSettingsCb, ResourceCb


class SourceKbBuilder:
    def __init__(self, channel_id: int):
        self.channel_id = channel_id
        self.kb = []

    def create_db_source_button(self):
        self.kb.append(
            [InlineKeyboardButton(text="📰 Даныне сервиса",
                                  callback_data=ResourceCb(
                                      channel_id=self.channel_id,
                                      resource=Resource.DATABASE,
                                      action="set",
                                  ).pack())]
        )

    def create_file_source_button(self):
        self.kb.append(
            [InlineKeyboardButton(text="📄 Свой файл",
                                  callback_data=ResourceCb(
                                      channel_id=self.channel_id,
                                      resource=Resource.FILE,
                                      action="set",
                                  ).pack())]
        )

    def create_ai_generate_source_button(self):
        self.kb.append(
            [InlineKeyboardButton(text="Сгенерированный файл",
                                  callback_data=ResourceCb(
                                      channel_id=self.channel_id,
                                      resource=Resource.AI_POSTS,
                                      action="set",
                                  ).pack())]
        )

    def create_back_button(self):
        self.kb.append(
            [InlineKeyboardButton(text="◀️ Назад",
                                  callback_data=ChannelSettingsCb(
                                      action="openMenu",
                                      channel_id=self.channel_id,
                                  ).pack())]
        )


class SourceKb:
    def __init__(self, data: ChannelSettings, payment_plan: PaymentOptions):
        self.data = data
        self.payment_plan = payment_plan
        self.builder = SourceKbBuilder(channel_id=self.data.channel_id)

    def get_kb(self):
        if self.payment_plan == PaymentOptions.PRO:
            if self.data.resource == Resource.DATABASE:
                self.builder.create_file_source_button()
            else:
                self.builder.create_db_source_button()
        elif self.payment_plan == PaymentOptions.VIP:
            if self.data.resource == Resource.DATABASE:
                self.builder.create_ai_generate_source_button()
                self.builder.create_file_source_button()
            elif self.data.resource == Resource.FILE:
                self.builder.create_ai_generate_source_button()
                self.builder.create_db_source_button()
            elif self.data.resource == Resource.AI_POSTS:
                self.builder.create_file_source_button()
                self.builder.create_db_source_button()
        self.builder.create_back_button()
        return InlineKeyboardMarkup(inline_keyboard=self.builder.kb)
