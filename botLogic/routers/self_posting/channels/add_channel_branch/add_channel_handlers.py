from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from .states.post_waiting import WaitPostOrId
from business_logic.services.channels_service.add_channel_facade import AddTgChannelFacade
from .keyboards.keyboard import get_back_button
from botLogic.common_bot_tools.callback_data import ChannelCb
from botLogic.common_bot_tools.tools.decorators import save_work

router = Router(name=__name__)


@router.callback_query(ChannelCb.filter(F.action == "addChannel"))
@save_work()
async def asking_for_post(call: CallbackQuery, state: FSMContext):
    buttons = get_back_button()
    await call.message.edit_text("📢 Перешлите любой пост из вашего Telegram-канала для его привязки.", reply_markup=buttons)
    await state.set_state(WaitPostOrId.wait_data)


@router.message(WaitPostOrId.wait_data)
@save_work()
async def handle_data(msg: Message):
    tg_id = msg.chat.id
    forward = msg.forward_from_chat
    facade = AddTgChannelFacade(forward_from=forward, tg_id=tg_id)
    text = await facade.add_channel()
    buttons = get_back_button()
    await msg.answer(text, reply_markup=buttons)
