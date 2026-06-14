from aiogram.fsm.context import FSMContext


async def clean_state(state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
