from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_self_buy_buttons():
    kb = [
        [InlineKeyboardButton(text="Да", callback_data="self_buy_on")],
        [InlineKeyboardButton(text="Нет", callback_data="self_buy_off")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)
