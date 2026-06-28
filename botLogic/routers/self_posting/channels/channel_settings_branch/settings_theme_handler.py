from aiogram import Router, F
from aiogram.types import CallbackQuery

from business_logic.services.channels_service.channel_settings_service import ChannelSettingsService
from business_logic.entities.channel_entity import PostTheme
from .keyboards.theme_kb import get_theme_kb, get_back_button_to_settings
from botLogic.common_bot_tools.callback_data import ChannelSettingsCb, ThemeCb

router = Router(name=__name__)


@router.callback_query(ChannelSettingsCb.filter(F.action == "openThemeMenu"))
async def theme_menu(call: CallbackQuery, callback_data: ChannelSettingsCb):
    channel_id = callback_data.channel_id
    service = ChannelSettingsService()
    data = await service.get_channel_settings(channel_id=channel_id, tg_id=call.message.chat.id)
    buttons = get_theme_kb(channel_id=channel_id, theme=data.theme)
    await call.message.edit_text("Выбери желаемую тему поста из списка", reply_markup=buttons)


@router.callback_query(ThemeCb.filter(F.action == "set"))
async def set_theme(call: CallbackQuery, callback_data: ThemeCb):
    channel_service = ChannelSettingsService()
    channel_id = callback_data.channel_id
    theme = PostTheme.enum_value(kb_value=callback_data.theme)
    channel = await channel_service.get_channel_settings(channel_id=channel_id, tg_id=call.message.chat.id)
    channel.theme = theme
    await channel_service.update_channel_settings(channel=channel)
    buttons = get_back_button_to_settings(channel_id=channel_id)
    await call.message.edit_text("Тема успешно установлена !", reply_markup=buttons)
