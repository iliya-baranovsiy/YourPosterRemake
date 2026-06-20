from aiogram import Router
from aiogram.types.message import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from ..common_bot_tools.keyboards.main_menu_kb import get_main_menu_kb
from business_logic.services.user_service import UserService

router = Router(name=__name__)


@router.message(CommandStart())
async def start_dialog(msg: Message, state: FSMContext):
    await state.clear()
    user_service = UserService()
    await user_service.create_user(tg_id=msg.chat.id, username=msg.chat.username)
    buttons = get_main_menu_kb()
    await msg.answer("Приветственное сообщение")
    await msg.answer("Главное меню", reply_markup=buttons)
