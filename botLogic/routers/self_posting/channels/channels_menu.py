from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from business_logic.services.channels_service.channels_service import ChannelsService
from .keyboards.menu_kb import MenuKb
from botLogic.common_bot_tools.tools.decorators import save_work

router = Router(name=__name__)


@router.callback_query(F.data == "channels")
@save_work()
async def get_channels_menu(call: CallbackQuery, state: FSMContext):
    await state.clear()
    service = ChannelsService()
    data = await service.get_channels(owner_id=call.message.chat.id)
    menu_kb = MenuKb(data=data)
    buttons = menu_kb.create_kb()
    await call.message.edit_text(
        f"Мои каналы\nДоступно для привязки: {data.channels_available_count - data.channels_count}",
        reply_markup=buttons)
