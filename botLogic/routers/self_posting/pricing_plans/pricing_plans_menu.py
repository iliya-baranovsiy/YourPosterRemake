from aiogram import F, Router
from aiogram.types.callback_query import CallbackQuery

from business_logic.services.user_service import UserService
from .function_tools.texts import get_pricing_plan_text
from .keyboards.plans_kb import get_plans_kb

router = Router(name=__name__)


@router.callback_query(F.data == "plans")
async def payments_plans_menu(call: CallbackQuery):
    user_service = UserService()
    user = await user_service.get_user(call.message.chat.id)
    text = get_pricing_plan_text(user)
    buttons = get_plans_kb(user.automatic_buy)
    await call.message.edit_text("Меню тарифов, твои текущие данные:\n" + text, reply_markup=buttons)
