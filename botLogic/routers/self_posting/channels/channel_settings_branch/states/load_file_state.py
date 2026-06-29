from aiogram.fsm.state import State, StatesGroup


class LoadFileState(StatesGroup):
    wait_file_loading = State()
