from aiogram import Router, F
from aiogram.types import CallbackQuery

from business_logic.services.channels_service.channel_settings_service import ChannelSettingsService
from business_logic.services.user_service import UserService
from business_logic.entities.channel_entity import PostTheme
from .keyboards.settings_kb import SettingsKb
from .function_tools.text import SettingsMenuText
from .keyboards.theme_kb import get_theme_kb, get_back_button_to_settings

router = Router(name=__name__)


@router.callback_query(F.data.startswith("settings"))
async def settings_menu_handler(call: CallbackQuery):
    channel_id = int(call.data.split("_")[1])
    channel_service = ChannelSettingsService()
    user_service = UserService()
    payment_plan = await user_service.get_only_payment_plan(tg_id=call.message.chat.id)
    channel_data = await channel_service.get_channel_settings(channel_id=channel_id)
    kb = SettingsKb(channel_id=channel_id, payment_plan=payment_plan, is_active=channel_data.posting_is_active)
    text_cls = SettingsMenuText(theme=channel_data.theme,
                                is_active=channel_data.posting_is_active,
                                payment_plan=payment_plan,
                                source=channel_data.resource)
    text = text_cls.get_text()
    buttons = kb.get_kb()
    await call.message.edit_text(text=text, reply_markup=buttons)


@router.callback_query(F.data.startswith("theme"))
async def theme_menu(call: CallbackQuery):
    channel_id = int(call.data.split("_")[1])
    service = ChannelSettingsService()
    data = await service.get_channel_settings(channel_id=channel_id)
    buttons = get_theme_kb(channel_id=channel_id, theme=data.theme)
    await call.message.edit_text("Выбери желаемую тему поста из списка", reply_markup=buttons)


@router.callback_query(F.data.startswith("settheme"))
async def set_theme(call: CallbackQuery):
    channel_service = ChannelSettingsService()
    data = call.data.split("_")
    channel_id = int(data[2])
    theme = PostTheme.enum_value(kb_value=data[1])
    channel = await channel_service.get_channel_settings(channel_id=channel_id)
    channel.theme = theme
    await channel_service.update_channel_settings(channel=channel)
    buttons = get_back_button_to_settings(channel_id=channel_id)
    await call.message.edit_text("Тема успешно установлена !", reply_markup=buttons)
