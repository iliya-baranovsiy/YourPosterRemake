from aiogram.fsm.state import State, StatesGroup


class PricingState(StatesGroup):
    confirm_to_pay = State()
