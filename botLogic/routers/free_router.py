from aiogram import Router
from aiogram.filters.state import StateFilter
from aiogram.types.message import Message
from botLogic.common_bot_tools.keyboards.main_menu_kb import get_main_menu_kb
from botLogic.common_bot_tools.tools.decorators import save_work

router = Router(name=__name__)


@router.message(StateFilter(None))
@save_work()
async def free_message(msg: Message):
    buttons = get_main_menu_kb()
    await msg.answer("Не знаю такой команды, вот меню", reply_markup=buttons)
