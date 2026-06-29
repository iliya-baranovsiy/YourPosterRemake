from aiogram import Router, F
from aiogram.types import CallbackQuery

from botLogic.common_bot_tools.callback_data import ChannelSettingsCb, LoadCb
from .keyboards.load_file_kb import LoadFileKb
from business_logic.services.channels_service.extension_service import ExtensionService
from business_logic.services.channels_service.channel_settings_service import ChannelSettingsService
from business_logic.common_options.status_option import Status
from .keyboards.theme_kb import get_back_button_to_settings

router = Router(name=__name__)


@router.callback_query(ChannelSettingsCb.filter(F.action == "loadFileMenu"))
async def request_to_load_file_menu(call: CallbackQuery, callback_data: ChannelSettingsCb):
    channel_id = callback_data.channel_id
    ext_service = ExtensionService()
    channel_service = ChannelSettingsService()
    channel = await channel_service.get_channel_settings(channel_id=channel_id, tg_id=call.message.chat.id)
    status = await ext_service.request_to_load_file(channel_id=channel_id, tg_id=call.message.chat.id)
    buttons = LoadFileKb(channel_id=channel_id, status=status, file_posts_count=channel.file_posts_count).get_kb()
    await call.message.edit_text("Выбери один из пунктов меню", reply_markup=buttons)


@router.callback_query(LoadCb.filter(F.action == "delete"))
async def request_to_delete(call: CallbackQuery, callback_data: LoadCb):
    channel_id = callback_data.channel_id
    ext_service = ExtensionService()
    status = await ext_service.delete_file_records(channel_id=channel_id, tg_id=call.message.chat.id)
    buttons = get_back_button_to_settings(channel_id=channel_id)
    if status == Status.OK:
        await call.message.edit_text("Удалено успешно", reply_markup=buttons)
    else:
        await call.message.edit_text("Что-то пошло не так", reply_markup=buttons)
