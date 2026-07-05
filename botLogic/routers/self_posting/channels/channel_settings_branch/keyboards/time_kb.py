from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.payments.options import PaymentOptions, PLAN_INFO
from botLogic.common_bot_tools.callback_data import TimeCb, ChannelSettingsCb


class TimeKbBuilder:
    def __init__(self, channel_id: int):
        self.kb = []
        self.channel_id = channel_id

    def create_time_button(self, time_to_show: str, time_to_cl: str):
        self.kb.append(
            [InlineKeyboardButton(text=f"{time_to_show}",
                                  callback_data=TimeCb(
                                      channel_id=self.channel_id,
                                      time_=time_to_cl,
                                      action="openTime",
                                  ).pack())]
        )

    def create_add_time_button(self):
        self.kb.append(
            [InlineKeyboardButton(text="➕ Добавить время",
                                  callback_data=TimeCb(
                                      channel_id=self.channel_id,
                                      time_="undefined",
                                      action="addTime",
                                  ).pack())]
        )

    def create_back_button(self):
        self.kb.append(
            [InlineKeyboardButton(text="◀️ Назад",
                                  callback_data=ChannelSettingsCb(
                                      channel_id=self.channel_id,
                                      action="openMenu", ).pack())]
        )


class TimeKb:
    def __init__(self, channel_id: int, times: list[str], payment_plan: PaymentOptions):
        self.channel_id = channel_id
        self.times = times
        self.payment_plan = payment_plan
        self.builder = TimeKbBuilder(channel_id=self.channel_id)

    def get_time_kb(self):
        if self.times:
            for time_ in self.times:
                time_to_cl = time_.replace(":", "-")
                self.builder.create_time_button(time_to_show=time_, time_to_cl=time_to_cl)
        if len(self.times) < PLAN_INFO[self.payment_plan].posts_count:
            self.builder.create_add_time_button()
        self.builder.create_back_button()
        return InlineKeyboardMarkup(inline_keyboard=self.builder.kb)


def back_to_time_menu(channel_id: int):
    kb = [
        [InlineKeyboardButton(text="◀️ Назад", callback_data=ChannelSettingsCb(
            action="openTimeList",
            channel_id=channel_id, ).pack())]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def request_to_delete_time(channel_id: int, time_: str):
    time_to_cl = time_.replace(":", "-")
    kb = [
        [
            InlineKeyboardButton(text="✅ Удалить",
                                 callback_data=TimeCb(
                                     channel_id=channel_id,
                                     time_=time_to_cl,
                                     action="dropTime",
                                 ).pack()),
            InlineKeyboardButton(text="❌ Отмена", callback_data=ChannelSettingsCb(
                action="openTimeList",
                channel_id=channel_id, ).pack())
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)
