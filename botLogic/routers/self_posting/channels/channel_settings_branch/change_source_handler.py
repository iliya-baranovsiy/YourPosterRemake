from aiogram import Router, F
from aiogram.types.callback_query import CallbackQuery

from botLogic.common_bot_tools.callback_data import ChannelSettingsCb, ResourceCb
from .keyboards.source_kb import SourceKb
from business_logic.services.channels_service.channel_settings_service import ChannelSettingsService
from business_logic.services.user_service import UserService
from .keyboards.theme_kb import get_back_button_to_settings

router = Router(name=__name__)


async def get_change_source_menu(call: CallbackQuery, channel_id: int, tg_id: int):
    channel_settings_service = ChannelSettingsService()
    user_service = UserService()
    payment_plan = await user_service.get_only_payment_plan(tg_id=tg_id)
    channel_settings = await channel_settings_service.get_channel_settings(channel_id=channel_id,
                                                                           tg_id=tg_id)
    buttons = SourceKb(data=channel_settings, payment_plan=payment_plan).get_kb()
    await call.message.edit_text(text="Доступные ресурсы", reply_markup=buttons)


@router.callback_query(ChannelSettingsCb.filter(F.action == "changeSource"))
async def change_source_menu_handler(call: CallbackQuery, callback_data: ChannelSettingsCb):
    await get_change_source_menu(call=call, channel_id=callback_data.channel_id, tg_id=call.message.chat.id)


@router.callback_query(ResourceCb.filter(F.action == "set"))
async def set_source_handler(call: CallbackQuery, callback_data: ResourceCb):
    channel_id = callback_data.channel_id
    wishful_resource = callback_data.resource
    channel_settings_service = ChannelSettingsService()
    channel = await channel_settings_service.get_channel_settings(channel_id=channel_id, tg_id=call.message.chat.id)
    try:
        channel.resource = wishful_resource
        await channel_settings_service.update_channel_settings(channel)
        await get_change_source_menu(call=call, channel_id=channel_id, tg_id=call.message.chat.id)
        await call.answer(text="Ресурс изменен", show_alert=True)
    except Exception as e:
        buttons = get_back_button_to_settings(channel_id=channel_id)
        await call.message.edit_text("Упс, что-то пошло не так", reply_markup=buttons)
