from aiogram import F, Router
from aiogram.types.callback_query import CallbackQuery
from aiogram.fsm.context import FSMContext

from business_logic.services.user_service import UserService
from business_logic.common_options.status_option import Status
from .function_tools.texts import get_pricing_plan_text, get_un_success_text
from .keyboards.plans_kb import get_plans_kb, get_back_to_plans
from business_logic.services.subscribe_service.subscribe_service import SubscribeService
from .keyboards.confirm_pay_kb import get_confirm_kb
from botLogic.common_bot_tools.tools.state_cleaner import clean_state
from .states.pricing_state import PricingState

router = Router(name=__name__)


async def get_payments_plans_menu(call: CallbackQuery, state: FSMContext):
    await clean_state(state)
    user_service = UserService()
    user = await user_service.get_user(call.message.chat.id)
    text = get_pricing_plan_text(user)
    buttons = get_plans_kb(user.automatic_buy)
    await call.message.edit_text("Меню тарифов, твои текущие данные:\n" + text, reply_markup=buttons)


@router.callback_query(F.data == "payment_plans")
async def payments_plans_menu(call: CallbackQuery, state: FSMContext):
    await get_payments_plans_menu(call=call, state=state)


@router.callback_query(F.data.startswith("plan"))
async def handle_wishful_plan(call: CallbackQuery, state: FSMContext):
    wishful_plan = call.data.split("_")[1]
    service = SubscribeService()
    data = await service.get_confirmation_data(tg_id=call.message.chat.id, new_plan=wishful_plan)
    buttons = get_confirm_kb()
    await state.set_state(PricingState.confirm_to_pay)
    await state.update_data(new_plan=wishful_plan, action=data.action)
    await call.message.edit_text(text=data.text, reply_markup=buttons)


@router.callback_query(F.data == "confirm", PricingState.confirm_to_pay)
async def confirm_handler(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    new_plan = state_data.get("new_plan")
    action = state_data.get("action")
    await clean_state(state)
    subscribe_service = SubscribeService()
    status = await subscribe_service.change_payment_plan(new_plan=new_plan, action=action, tg_id=call.message.chat.id)

    if status == Status.OK:
        buttons = get_back_to_plans()
        await call.message.edit_text("Успех", reply_markup=buttons)
    else:
        buttons = get_back_to_plans()
        text = get_un_success_text()
        await call.message.edit_text(text, reply_markup=buttons)


@router.callback_query(F.data == "not_confirm")
async def not_confirm_handler(call: CallbackQuery, state: FSMContext):
    await get_payments_plans_menu(call=call, state=state)
