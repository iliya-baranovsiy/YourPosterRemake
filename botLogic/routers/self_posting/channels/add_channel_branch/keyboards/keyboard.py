from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_back_button():
    kb = [
        [InlineKeyboardButton(text="◀️ Назад", callback_data="channels")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)
