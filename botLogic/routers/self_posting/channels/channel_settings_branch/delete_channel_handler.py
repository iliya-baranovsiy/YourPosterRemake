from aiogram import Router, F
from aiogram.types import CallbackQuery

from .keyboards.request_kb import get_request_kb_for_delete
from ..add_channel_branch.keyboards.keyboard import get_back_button
from business_logic.services.channels_service.channels_service import ChannelsService

router = Router(name=__name__)


@router.callback_query(F.data.startswith("delete"))
async def request_to_delete(call: CallbackQuery):
    channel_id = int(call.data.split("_")[1])
    buttons = get_request_kb_for_delete(channel_id=channel_id)
    await call.message.edit_text("Ты действительно хочешь отвязать этот канал ?", reply_markup=buttons)


@router.callback_query(F.data.startswith("drop"))
async def drop_channel(call: CallbackQuery):
    channel_id = int(call.data.split("_")[1])
    channel_service = ChannelsService()
    await channel_service.delete_channel(channel_id=channel_id, owner_id=call.message.chat.id)
    buttons = get_back_button()
    await call.message.edit_text("Твой канал успешно отвязан", reply_markup=buttons)
