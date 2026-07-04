from pathlib import Path
from aiogram import Router
from aiogram.types.message import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile

from ..common_bot_tools.tools.decorators import save_work
from ..common_bot_tools.keyboards.main_menu_kb import get_main_menu_kb
from business_logic.services.user_service import UserService
from botLogic.common_bot_tools.tools.hello_text import hello, main_menu

router = Router(name=__name__)


@router.message(CommandStart())
@save_work()
async def start_dialog(msg: Message, state: FSMContext):
    await state.clear()
    user_service = UserService()
    await user_service.create_user(tg_id=msg.chat.id, username=msg.chat.username)
    buttons = get_main_menu_kb()
    await msg.answer_photo(caption=hello,
                           photo=FSInputFile(path=Path("botLogic") / "src" / "logo.png"))
    await msg.answer(text=main_menu, reply_markup=buttons)
