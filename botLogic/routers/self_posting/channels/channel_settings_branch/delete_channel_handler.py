from aiogram import Router, F
from aiogram.types import CallbackQuery

from .keyboards.request_kb import get_request_kb_for_delete
from ..add_channel_branch.keyboards.keyboard import get_back_button
from business_logic.services.channels_service.channels_service import ChannelsService
from botLogic.common_bot_tools.callback_data import ChannelCb
from botLogic.common_bot_tools.tools.decorators import save_work

router = Router(name=__name__)


@router.callback_query(ChannelCb.filter(F.action == "requestToDrop"))
@save_work()
async def request_to_delete(call: CallbackQuery, callback_data: ChannelCb):
    channel_id = callback_data.channel_id
    buttons = get_request_kb_for_delete(channel_id=channel_id)
    await call.message.edit_text("🔌 Отвязать канал?\n\nПосле подтверждения канал будет удален из YourPoster.",
                                 reply_markup=buttons)


@router.callback_query(ChannelCb.filter(F.action == "deleteChannel"))
@save_work()
async def drop_channel(call: CallbackQuery, callback_data: ChannelCb):
    channel_id = callback_data.channel_id
    channel_service = ChannelsService()
    await channel_service.delete_channel(channel_id=channel_id, owner_id=call.message.chat.id)
    buttons = get_back_button()
    await call.message.edit_text("Твой канал успешно отвязан", reply_markup=buttons)
