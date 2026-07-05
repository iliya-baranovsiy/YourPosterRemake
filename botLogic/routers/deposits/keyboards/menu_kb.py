from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_deposits_menu_kb():
    kb = [
        [InlineKeyboardButton(text="Звезды", callback_data="stars_deposit")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)
