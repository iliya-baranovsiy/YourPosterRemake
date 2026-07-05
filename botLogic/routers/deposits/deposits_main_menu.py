from aiogram import Router, F
from aiogram.types import CallbackQuery

from .keyboards.menu_kb import get_deposits_menu_kb
from botLogic.common_bot_tools.tools.decorators import save_work

router = Router(name=__name__)


@router.callback_query(F.data == "payments_menu")
@save_work()
async def get_deposits_menu(call: CallbackQuery):
    buttons = get_deposits_menu_kb()
    await call.message.edit_text("Выберите способ оплаты", reply_markup=buttons)
