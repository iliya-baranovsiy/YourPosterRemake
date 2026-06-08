from aiogram import Router
from aiogram.types.message import Message
from aiogram.filters import CommandStart

from ..common_bot_tools.keyboards.main_menu_kb import get_main_menu_kb
from business_logic.entities.user_entity import User
from business_logic.repositories.user_repository import UserRepository

router = Router(name=__name__)


@router.message(CommandStart())
async def start_dialog(msg: Message):
    user = User(tg_id=msg.chat.id, username='@' + msg.chat.username)
    user_repo = UserRepository(user)
    await user_repo.create_record()
    buttons = get_main_menu_kb()
    await msg.answer("Приветственное сообщение")
    await msg.answer("Главное меню", reply_markup=buttons)
