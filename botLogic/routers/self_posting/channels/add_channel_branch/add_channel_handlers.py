from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from .states.post_waiting import WaitPostOrId
from .functions_tools.add_channel_logic import AddTgChannelFacade
from .keyboards.keyboard import get_back_button

router = Router(name=__name__)


@router.callback_query(F.data == "add_channel")
async def asking_for_post(call: CallbackQuery, state: FSMContext):
    buttons = get_back_button()
    await call.message.edit_text("Перешли мне пост со своего канала для привязки", reply_markup=buttons)
    await state.set_state(WaitPostOrId.wait_data)


@router.message(WaitPostOrId.wait_data)
async def handle_data(msg: Message):
    tg_id = msg.chat.id
    forward = msg.forward_from_chat
    facade = AddTgChannelFacade(forward_from=forward, tg_id=tg_id)
    text = await facade.add_channel()
    buttons = get_back_button()
    await msg.answer(text, reply_markup=buttons)
