from aiogram import Router, F
from aiogram.types import CallbackQuery

from .keyboards.main_menu_kb import MenuKb
from business_logic.services.channels_service.channel_settings_service import ChannelSettingsService
from .function_tools.text import get_settings_menu_text

router = Router(name=__name__)


@router.callback_query(F.data.startswith("channel"))
async def channel_settings_main_menu(call: CallbackQuery):
    call_data = call.data.split("_")
    channel_id = int(call_data[1])
    channel_set_service = ChannelSettingsService()
    settings = await channel_set_service.get_channel_settings(channel_id=channel_id)
    kb_instance = MenuKb(channel_id=channel_id)
    buttons = kb_instance.get_kb()
    text = get_settings_menu_text(settings)
    await call.message.edit_text(text=text, reply_markup=buttons)
