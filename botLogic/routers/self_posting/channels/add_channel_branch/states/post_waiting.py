from aiogram.fsm.state import State, StatesGroup


class WaitPostOrId(StatesGroup):
    wait_data = State()
