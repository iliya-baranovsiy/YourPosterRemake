from aiogram import Router, F
from aiogram.types.callback_query import CallbackQuery

from .commom_self_posting_tools.keyboards.self_posting_menu_kb import get_self_posting_menu_kb
from business_logic.services.user_service import UserService
from .commom_self_posting_tools.help_functions.menu_text import get_menu_text

router = Router(name=__name__)


@router.callback_query(F.data == "autoposting_menu")
async def self_posting_menu(call: CallbackQuery):
    user_service = UserService()
    user = await user_service.get_user(call.message.chat.id)
    text = get_menu_text(user)
    buttons = get_self_posting_menu_kb()
    await call.message.edit_text("Меню автопостинга\n" + text, reply_markup=buttons)
