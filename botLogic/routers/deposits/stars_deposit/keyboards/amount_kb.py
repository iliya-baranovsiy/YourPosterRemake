from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from botLogic.common_bot_tools.callback_data import StarsDepositCb


def get_amount_stars_kb():
    kb = [
        [InlineKeyboardButton(text="130 🌟 ~ 3.1$", callback_data=StarsDepositCb(amount=130).pack())],
        [InlineKeyboardButton(text="260 🌟 ~ 6.2$", callback_data=StarsDepositCb(amount=260).pack())],
        [InlineKeyboardButton(text="520 🌟 ~ 12.4$", callback_data=StarsDepositCb(amount=520).pack())],
        [InlineKeyboardButton(text="Назад", callback_data="payments_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)


def get_pay_kb(amount: int):
    kb = []
    if amount == 130:
        kb.append([InlineKeyboardButton(text="Оплатить 130 🌟", pay=True)])
    elif amount == 260:
        kb.append([InlineKeyboardButton(text="Оплатить 260 🌟", pay=True)])
    elif amount == 520:
        kb.append([InlineKeyboardButton(text="Оплатить 520 🌟", pay=True)])
    kb.append([InlineKeyboardButton(text="Назад", callback_data="stars_deposit")])
    return InlineKeyboardMarkup(inline_keyboard=kb)


def get_main_menu_button():
    kb = [
        [InlineKeyboardButton(text="◀️ Назад", callback_data="back_to_main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)
