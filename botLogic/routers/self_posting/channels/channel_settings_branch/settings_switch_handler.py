from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from business_logic.services.channels_service.channel_settings_service import ChannelSettingsService
from botLogic.common_bot_tools.callback_data import ChannelSettingsCb
from .settings_menu_handler import get_settings_menu
from botLogic.common_bot_tools.tools.decorators import save_work

router = Router(name=__name__)


@router.callback_query(ChannelSettingsCb.filter(F.action == "activatePosting"))
@save_work()
async def activate_self_posting(call: CallbackQuery, callback_data: ChannelSettingsCb, state: FSMContext):
    channels_set_srvice = ChannelSettingsService()
    channel_id = callback_data.channel_id
    channel = await channels_set_srvice.get_channel_settings(channel_id=channel_id, tg_id=call.message.chat.id)
    channel.posting_is_active = True
    await channels_set_srvice.update_channel_settings(channel)
    await get_settings_menu(call=call, channel_id=channel_id, state=state)
    await call.answer(text="Постинг активирован", show_alert=True)


@router.callback_query(ChannelSettingsCb.filter(F.action == "deactivatePosting"))
@save_work()
async def deactivate_self_posting(call: CallbackQuery, callback_data: ChannelSettingsCb, state: FSMContext):
    channels_set_srvice = ChannelSettingsService()
    channel_id = callback_data.channel_id
    channel = await channels_set_srvice.get_channel_settings(channel_id=channel_id, tg_id=call.message.chat.id)
    channel.posting_is_active = False
    await channels_set_srvice.update_channel_settings(channel)
    await get_settings_menu(call=call, channel_id=channel_id, state=state)
    await call.answer(text="Постинг выключен", show_alert=True)
