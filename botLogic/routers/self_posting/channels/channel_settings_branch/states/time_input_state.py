from aiogram.fsm.state import State, StatesGroup


class WaitTime(StatesGroup):
    wait_time_input = State()
