from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_self_posting_menu_kb():
    kb = [
        [InlineKeyboardButton(text="Мои каналы", callback_data="channels")],
        [InlineKeyboardButton(text="Тарифы", callback_data="payment_plans")],
        # [InlineKeyboardButton(text="Узнать id канала", callback_data="channel_id")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_main_menu")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=kb)
