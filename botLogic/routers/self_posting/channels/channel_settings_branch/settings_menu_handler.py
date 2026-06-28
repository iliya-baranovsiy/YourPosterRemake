from aiogram import Router, F
from aiogram.types import CallbackQuery

from business_logic.services.channels_service.channel_settings_service import ChannelSettingsService
from business_logic.services.user_service import UserService
from .keyboards.settings_kb import SettingsKb
from .function_tools.text import SettingsMenuText
from botLogic.common_bot_tools.callback_data import ChannelSettingsCb

router = Router(name=__name__)


async def get_settings_menu(call: CallbackQuery, channel_id: int):
    channel_service = ChannelSettingsService()
    user_service = UserService()
    payment_plan = await user_service.get_only_payment_plan(tg_id=call.message.chat.id)
    channel_data = await channel_service.get_channel_settings(channel_id=channel_id, tg_id=call.message.chat.id)
    kb = SettingsKb(channel_id=channel_id, payment_plan=payment_plan, is_active=channel_data.posting_is_active,
                    theme=channel_data.theme, resource=channel_data.resource)
    text_cls = SettingsMenuText(theme=channel_data.theme,
                                is_active=channel_data.posting_is_active,
                                payment_plan=payment_plan,
                                source=channel_data.resource)
    text = text_cls.get_text() or "test text"
    buttons = kb.get_kb()
    await call.message.edit_text(text=text, reply_markup=buttons)


@router.callback_query(ChannelSettingsCb.filter(F.action == "openMenu"))
async def settings_menu_handler(call: CallbackQuery, callback_data: ChannelSettingsCb):
    channel_id = callback_data.channel_id
    await get_settings_menu(call=call, channel_id=channel_id)
