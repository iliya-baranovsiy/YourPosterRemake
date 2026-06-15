from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from ..function_tools.keyboard_builder import Keyboard


def get_plans_kb(user):
    kb = Keyboard()
    buttons = kb.get_kb(user)
    return buttons


def get_back_to_plans():
    kb = [
        [InlineKeyboardButton(text="Назад", callback_data="payment_plans")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)
