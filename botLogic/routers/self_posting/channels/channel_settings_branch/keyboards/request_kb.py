from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_request_kb_for_delete(channel_id: int) -> InlineKeyboardMarkup:
    kb = [
        [
            InlineKeyboardButton(text="Да", callback_data=f"drop_{channel_id}"),
            InlineKeyboardButton(text="Нет", callback_data=f"channel_{channel_id}")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def back_button():
    kb = [
        [InlineKeyboardButton(text="Назад", callback_data="channels")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)
