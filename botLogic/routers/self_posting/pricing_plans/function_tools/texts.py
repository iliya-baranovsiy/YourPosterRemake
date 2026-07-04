from business_logic.entities.user_entity import User
from business_logic.entities.payment_plan_entity import Action
from business_logic.common_options.status_option import DescriptionStatus
from business_logic.common_options.status_option import Status
from ..keyboards.self_buy_question import get_self_buy_buttons
from ..keyboards.plans_kb import get_back_to_plans
from ..entities.answer_entity import Answer
from database.payments.options import PaymentOptions


def get_pricing_plan_text(user: User) -> str:
    text = (f"⭐ <b>Текущий тариф:</b> {user.subscription.payment_plan_str}\n"
            f"📅 <b>Активен до:</b> {user.subscription.end_date}\n"
            f"💰 <b>Баланс:</b> {user.balance}$\n"
            f"🔄 <b>Автопродление:</b> {'вкл' if user.automatic_buy else 'выкл'}\n"
            f"Выберите действие ниже.\n")
    if user.subscription.pending_plan != user.subscription.payment_plan and user.subscription.pending_plan != PaymentOptions.STANDART:
        text += f"<b>Запланирован переход к тарифу {user.subscription.pending_plan.value}</b>"
    return text


def get_result_answer(description: DescriptionStatus) -> Answer:
    if description.status == Status.OK and description.action == Action.RENEW:
        """RENEW"""
        text = f"✅ Подписка успешно продлена!\n\nСпасибо за использование YourPoster. Приятной работы! 🚀"
        buttons = get_back_to_plans()
        return Answer(text=text, buttons=buttons)
    elif description.status == Status.OK and description.action != Action.DOWNGRADE:
        """BUY/UPGRADE"""
        text = f"🔄 Включить автопродление подписки?\n\nПри включенном автопродлении стоимость тарифа будет автоматически списываться с вашего баланса при окончании текущего периода."
        buttons = get_self_buy_buttons()
        return Answer(text=text, buttons=buttons)
    elif description.status == Status.OK and description.action == Action.DOWNGRADE:
        "DOWNGRADE"
        text = "Отлично, твой тариф начнет действовать по истечению текущего"
        buttons = get_back_to_plans()
        return Answer(text=text, buttons=buttons)
    else:
        text = "❌ Не удалось выполнить операцию.\n\nПроверьте баланс и попробуйте снова."
        buttons = get_back_to_plans()
        return Answer(text=text, buttons=buttons)
