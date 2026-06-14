from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_confirm_kb():
    kb = [
        [InlineKeyboardButton(text="Да", callback_data="confirm")],
        [InlineKeyboardButton(text="Нет", callback_data="not_confirm")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)
