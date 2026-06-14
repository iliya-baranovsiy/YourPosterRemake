from aiogram import F, Router
from aiogram.types.callback_query import CallbackQuery

from business_logic.services.user_service import UserService
from .function_tools.texts import get_pricing_plan_text
from .keyboards.plans_kb import get_plans_kb
from business_logic.services.subscribe_service.subscribe_service import SubscribeService
from .keyboards.confirm_pay_kb import get_confirm_kb

router = Router(name=__name__)


@router.callback_query(F.data == "payment_plans")
async def payments_plans_menu(call: CallbackQuery):
    user_service = UserService()
    user = await user_service.get_user(call.message.chat.id)
    text = get_pricing_plan_text(user)
    buttons = get_plans_kb(user.automatic_buy)
    await call.message.edit_text("Меню тарифов, твои текущие данные:\n" + text, reply_markup=buttons)


@router.callback_query(F.data.startswith("plan"))
async def handle_wishful_plan(call: CallbackQuery):
    wishful_plan = call.data.split("_")[1]
    service = SubscribeService()
    data = await service.get_confirmation_data(tg_id=call.message.chat.id, new_plan=wishful_plan)
    buttons = get_confirm_kb()
    await call.message.edit_text(text=data.text, reply_markup=buttons)
