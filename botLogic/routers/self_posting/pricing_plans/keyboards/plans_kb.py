from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_plans_kb(self_buy: bool):
    if self_buy:
        self_buy_button = [InlineKeyboardButton(text="Выкл автопокупку", callback_data="self_buy_off")]
    else:
        self_buy_button = [InlineKeyboardButton(text="Вкл автопокупку", callback_data="self_buy_on")]
    kb = [
        [InlineKeyboardButton(text="VIP", callback_data="plan_VIP")],
        [InlineKeyboardButton(text="PRO", callback_data="plan_PRO")],
        self_buy_button,
        [InlineKeyboardButton(text="Назад", callback_data="autoposting_menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def get_back_to_plans():
    kb = [
        [InlineKeyboardButton(text="Назад", callback_data="payment_plans")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)
