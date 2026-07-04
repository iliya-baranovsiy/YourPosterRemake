from aiogram import Router, F
from aiogram.types import CallbackQuery

from .keyboards.main_menu_kb import MenuKb
from business_logic.services.channels_service.channel_settings_service import ChannelSettingsService
from .function_tools.text import get_settings_menu_text
from botLogic.common_bot_tools.callback_data import ChannelCb
from botLogic.common_bot_tools.tools.decorators import save_work

router = Router(name=__name__)


@router.callback_query(ChannelCb.filter(F.action == "openChannelMenu"))
@save_work()
async def channel_settings_main_menu(call: CallbackQuery, callback_data: ChannelCb):
    channel_id = callback_data.channel_id
    channel_set_service = ChannelSettingsService()
    settings = await channel_set_service.get_channel_settings(channel_id=channel_id, tg_id=call.message.chat.id)
    kb_instance = MenuKb(channel_id=channel_id)
    buttons = kb_instance.get_kb()
    text = get_settings_menu_text(settings)
    await call.message.edit_text(text=text, reply_markup=buttons)
