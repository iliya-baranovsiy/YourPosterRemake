from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.payments.options import PaymentOptions, PLAN_INFO


class TimeKbBuilder:
    def __init__(self, channel_id: int):
        self.kb = []
        self.channel_id = channel_id

    def create_time_button(self, time_: str):
        self.kb.append(
            [InlineKeyboardButton(text=f"{time_}", callback_data=f"chtime_{self.channel_id}_{time_}")]
        )

    def create_add_time_button(self):
        self.kb.append(
            [InlineKeyboardButton(text="Добавить время", callback_data=f"inserttime_{self.channel_id}")]
        )

    def create_back_button(self):
        self.kb.append(
            [InlineKeyboardButton(text="Назад", callback_data=f"settings_{self.channel_id}")]
        )


class TimeKb:
    def __init__(self, channel_id: int, times: list, payment_plan: PaymentOptions):
        self.channel_id = channel_id
        self.times = times
        self.payment_plan = payment_plan
        self.builder = TimeKbBuilder(channel_id=self.channel_id)

    def get_time_kb(self):
        if self.times:
            for time_ in self.times:
                self.builder.create_time_button(time_=time_)
        if len(self.times) < PLAN_INFO[self.payment_plan].posts_count:
            self.builder.create_add_time_button()
        self.builder.create_back_button()
        return InlineKeyboardMarkup(inline_keyboard=self.builder.kb)


def back_to_time_menu(channel_id: int):
    kb = [
        [InlineKeyboardButton(text="Назад", callback_data=f"timelist_{channel_id}")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def request_to_delete_time(channel_id: int, time_: str):
    kb = [
        [
            InlineKeyboardButton(text="Да", callback_data=f"dchanneltime_{channel_id}_{time_}"),
            InlineKeyboardButton(text="Нет", callback_data=f"timelist_{channel_id}")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)
