from aiogram import Router, F
from aiogram.types import CallbackQuery, LabeledPrice, PreCheckoutQuery, Message
from aiogram.fsm.context import FSMContext

from .keyboards.amount_kb import get_amount_stars_kb, get_pay_kb, get_main_menu_button
from botLogic.common_bot_tools.tools.decorators import save_work
from botLogic.common_bot_tools.callback_data import StarsDepositCb
from business_logic.services.payments_service.payments_stars_service import PaymentStarsService
from business_logic.common_options.status_option import Status
from botLogic.common_bot_tools.tools.state_cleaner import clean_state

router = Router(name=__name__)


@router.callback_query(F.data == "stars_deposit")
@save_work()
async def stars_amount_choice(call: CallbackQuery, state: FSMContext):
    await clean_state(state)
    buttons = get_amount_stars_kb()
    try:
        await call.message.edit_text("⭐ Пополнение через Telegram Stars\n\nВыберите сумму пополнения.",
                                     reply_markup=buttons)
    except:
        await call.message.delete()
        await call.message.answer("⭐ Пополнение через Telegram Stars\n\nВыберите сумму пополнения.",
                                  reply_markup=buttons)


@router.callback_query(StarsDepositCb.filter())
@save_work()
async def process_stars_deposit(call: CallbackQuery, callback_data: StarsDepositCb, state: FSMContext):
    amount = callback_data.amount
    prices = [LabeledPrice(label="Stars", amount=amount)]
    await call.message.delete()
    msg = await call.bot.send_invoice(
        chat_id=call.from_user.id,
        title="Пополнение баланса",
        description=f"Пополнение на {amount} ⭐",
        payload=f"stars_deposit_{amount}_{call.from_user.id}",
        provider_token="",
        currency="XTR",
        reply_markup=get_pay_kb(amount),
        prices=prices
    )
    await state.update_data(invoice_id=msg.message_id, invoice_chat_id=msg.chat.id)


@router.pre_checkout_query()
async def pre_checkout_handler(query: PreCheckoutQuery):
    await query.answer(ok=True)


@router.message(lambda m: m.successful_payment)
@save_work()
async def successful_payment(message: Message, state: FSMContext):
    state_data = await state.get_data()
    invoice_id = state_data.get("invoice_id")
    invoice_chat_id = state_data.get("invoice_chat_id")
    if invoice_id:
        try:
            await message.bot.delete_message(chat_id=invoice_chat_id, message_id=invoice_id)
        except:
            pass
    await clean_state(state)
    payment = message.successful_payment
    amount = payment.total_amount
    tg_charge_id = payment.telegram_payment_charge_id
    payload = payment.invoice_payload
    user_id = message.from_user.id
    pay_service = PaymentStarsService()
    status = await pay_service.pay(user_id=user_id, amount=amount, telegram_charge_id=tg_charge_id, payload=payload)
    if status == Status.OK:
        await message.answer(
            text=(
                f"✅ Платеж успешно выполнен.\n\n"
                f"Списано: <b>{amount} ⭐</b>.\n\n"
                "Для продолжения вернитесь в главное меню."
            ),
            reply_markup=get_main_menu_button()
        )
    else:
        await message.answer(
            text=(
                "⚠️ Не удалось подтвердить платеж.\n\n"
                "Если средства были списаны, но баланс не пополнился, "
                "обратитесь в поддержку.\n\n"
                "Для продолжения вернитесь в главное меню."
            ),
            reply_markup=get_main_menu_button()
        )
