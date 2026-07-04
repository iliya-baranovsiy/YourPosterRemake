from aiogram import Router, F
from aiogram.types.callback_query import CallbackQuery
from ..common_bot_tools.keyboards.main_menu_kb import get_main_menu_kb
from botLogic.common_bot_tools.tools.decorators import save_work
from botLogic.common_bot_tools.tools.hello_text import main_menu

router = Router(name=__name__)


@router.callback_query(F.data == "back_to_main_menu")
@save_work()
async def return_main_menu_kb(call: CallbackQuery):
    buttons = get_main_menu_kb()
    await call.message.edit_text(text=main_menu, reply_markup=buttons)
