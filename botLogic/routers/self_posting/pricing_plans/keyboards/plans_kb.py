from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_plans_kb(self_buy: bool):
    if self_buy:
        self_buy_button = [InlineKeyboardButton(text="Выкл автопокупку", callback_data="self_buy_off")]
    else:
        self_buy_button = [InlineKeyboardButton(text="Вкл автопокупку", callback_data="self_buy_on")]
    kb = [
        [InlineKeyboardButton(text="VIP", callback_data="VIP_plan")],
        [InlineKeyboardButton(text="PRO", callback_data="PRO_plan")],
        self_buy_button,
        [InlineKeyboardButton(text="Назад", callback_data="autoposting_menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)
