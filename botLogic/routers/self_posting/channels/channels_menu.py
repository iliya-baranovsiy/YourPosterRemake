from aiogram import F, Router
from aiogram.types import CallbackQuery

router = Router(name=__name__)


@router.callback_query(F.data == "channels")
async def get_channels_menu(call: CallbackQuery):
    await call.message.edit_text("Мои каналы")
