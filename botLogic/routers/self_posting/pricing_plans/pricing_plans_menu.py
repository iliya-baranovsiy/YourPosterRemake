from aiogram import F, Router
from aiogram.types.callback_query import CallbackQuery
from aiogram.fsm.context import FSMContext

from business_logic.services.user_service import UserService
from .function_tools.texts import get_pricing_plan_text, get_result_answer
from .keyboards.plans_kb import get_plans_kb, get_back_to_plans
from business_logic.services.subscribe_service.subscribe_service import SubscribeService
from .keyboards.confirm_pay_kb import get_confirm_kb
from botLogic.common_bot_tools.tools.state_cleaner import clean_state
from .states.pricing_state import PricingState
from botLogic.common_bot_tools.tools.decorators import save_work

router = Router(name=__name__)


async def get_payments_plans_menu(call: CallbackQuery, state: FSMContext):
    await clean_state(state)
    user_service = UserService()
    user = await user_service.get_user(call.message.chat.id)
    text = get_pricing_plan_text(user)
    buttons = get_plans_kb(user=user)
    await call.message.edit_text("💎 Управление тарифом\n" + text, reply_markup=buttons)


@router.callback_query(F.data == "payment_plans")
@save_work()
async def payments_plans_menu(call: CallbackQuery, state: FSMContext):
    await get_payments_plans_menu(call=call, state=state)


@router.callback_query(F.data.startswith("plan"))
@save_work()
async def handle_wishful_plan(call: CallbackQuery, state: FSMContext):
    wishful_plan = call.data.split("_")[1]
    service = SubscribeService()
    data = await service.get_confirmation_data(tg_id=call.message.chat.id, new_plan=wishful_plan)
    buttons = get_confirm_kb()
    await state.set_state(PricingState.confirm_to_pay)
    await state.update_data(new_plan=wishful_plan, action=data.action)
    await call.message.edit_text(text=data.text, reply_markup=buttons)


@router.callback_query(F.data == "confirm", PricingState.confirm_to_pay)
@save_work()
async def confirm_handler(call: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    new_plan = state_data.get("new_plan")
    action = state_data.get("action")
    await clean_state(state)
    subscribe_service = SubscribeService()
    status = await subscribe_service.change_payment_plan(new_plan=new_plan, action=action, tg_id=call.message.chat.id)
    answer = get_result_answer(status)
    await call.message.edit_text(text=answer.text, reply_markup=answer.buttons)


@router.callback_query(F.data == "not_confirm")
@save_work()
async def not_confirm_handler(call: CallbackQuery, state: FSMContext):
    await get_payments_plans_menu(call=call, state=state)


@router.callback_query(F.data == "self_buy_turn_on")
@save_work()
async def turn_on_self_buy(call: CallbackQuery):
    sub_service = SubscribeService()
    await sub_service.switch_on_self_buy(call.message.chat.id)
    buttons = get_back_to_plans()
    await call.message.edit_text(
        text="Тариф будет продлеваться атоматически, ты влюбое время можешь выключить эту функцию",
        reply_markup=buttons)


@router.callback_query(F.data.startswith("menu_self_buy_"))
@save_work()
async def switch_self_buy(call: CallbackQuery, state: FSMContext):
    wishful_position = call.data.split("_")[3]
    sub_service = SubscribeService()
    await sub_service.switch_self_buy(tg_id=call.message.chat.id, pending_operation=wishful_position)
    await get_payments_plans_menu(state=state, call=call)


@router.callback_query(F.data == "cancel_movement")
@save_work()
async def cancel_movement(call: CallbackQuery, state: FSMContext):
    sub_service = SubscribeService()
    await sub_service.cancel_movement(call.message.chat.id)
    await call.answer(text="Переход отменен", show_alert=True)
    await get_payments_plans_menu(call=call, state=state)
