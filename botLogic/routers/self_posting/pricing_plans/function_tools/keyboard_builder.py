from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.payments.options import PaymentOptions, PLAN_INFO
from business_logic.entities.user_entity import User


class KeyboardBuilder:
    def __init__(self):
        self.base_kb = []

    def add_vip_button(self):
        self.base_kb.append(
            [InlineKeyboardButton(text="VIP", callback_data="plan_VIP")]
        )

    def add_pro_button(self):
        self.base_kb.append(
            [InlineKeyboardButton(text="⭐ PRO", callback_data="plan_PRO")]
        )

    def add_switch_self_pay_btn(self, self_buy: bool):
        if self_buy:
            self.base_kb.append(
                [InlineKeyboardButton(text="🔄 Автопродление: выкл", callback_data="menu_self_buy_off")]
            )
        else:
            self.base_kb.append(
                [InlineKeyboardButton(text="🔄 Автопродление: вкл", callback_data="menu_self_buy_on")]
            )

    def add_off_move_button(self):
        self.base_kb.append(
            [InlineKeyboardButton(text="Отменить переход", callback_data="cancel_movement")]
        )

    def add_back_button(self):
        self.base_kb.append(
            [InlineKeyboardButton(text="Назад ◀️", callback_data="autoposting_menu")]
        )


class Keyboard:
    def __init__(self):
        self.builder = KeyboardBuilder()

    def get_kb(self, user: User):
        if ((user.subscription.pending_plan != PaymentOptions.STANDART) and
                (user.subscription.priority > PLAN_INFO[user.subscription.pending_plan].priority)):
            # self.builder.add_vip_button()
            self.builder.add_off_move_button()
            self.builder.add_back_button()
            return InlineKeyboardMarkup(inline_keyboard=self.builder.base_kb)
        elif user.subscription.payment_plan != PaymentOptions.STANDART:
            # self.builder.add_vip_button()
            self.builder.add_pro_button()
            self.builder.add_switch_self_pay_btn(self_buy=user.automatic_buy)
            self.builder.add_back_button()
            return InlineKeyboardMarkup(inline_keyboard=self.builder.base_kb)
        else:
            # self.builder.add_vip_button()
            self.builder.add_pro_button()
            self.builder.add_back_button()
            return InlineKeyboardMarkup(inline_keyboard=self.builder.base_kb)
