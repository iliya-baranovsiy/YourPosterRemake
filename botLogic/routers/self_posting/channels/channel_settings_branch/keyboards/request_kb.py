from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from botLogic.common_bot_tools.callback_data import ChannelCb


def get_request_kb_for_delete(channel_id: int) -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(text="Да",
                                 callback_data=ChannelCb(channel_id=channel_id, action="deleteChannel").pack()),
            InlineKeyboardButton(text="Нет",
                                 callback_data=ChannelCb(channel_id=channel_id, action="openChannelMenu").pack())
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)
