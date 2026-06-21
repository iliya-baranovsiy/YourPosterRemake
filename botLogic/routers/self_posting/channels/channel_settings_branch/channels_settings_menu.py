from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from .keyboards.main_menu_kb import MenuKb

router = Router(name=__name__)


@router.callback_query(F.data.startswith("channel"))
async def channel_settings_main_menu(call: CallbackQuery):
    call_data = call.data.split("_")
    channel_id = int(call_data[1])
    kb_instance = MenuKb(channel_id=channel_id)
    buttons = kb_instance.get_kb()
    await call.message.edit_text(text="Меню канала", reply_markup=buttons)
