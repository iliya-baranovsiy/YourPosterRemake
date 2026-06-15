from business_logic.entities.user_entity import User
from business_logic.entities.payment_plan_entity import Action
from business_logic.common_options.status_option import DescriptionStatus
from business_logic.common_options.status_option import Status
from ..keyboards.self_buy_question import get_self_buy_buttons
from ..keyboards.plans_kb import get_back_to_plans
from ..entities.answer_entity import Answer


def get_pricing_plan_text(user: User) -> str:
    text = (f"<b>Тариф:</b> {user.subscription.payment_plan_str}\n"
            f"<b>Действует по:</b> {user.subscription.end_date}\n"
            f"<b>Баланс:</b> {user.balance}")
    return text


def get_un_success_text() -> str:
    text = "Упс, что-то пошло не так, проверь средства на балансе и попробуй заново"
    return text


def get_result_answer(description: DescriptionStatus) -> Answer:
    if description.status == Status.OK and description.action == Action.RENEW:
        """RENEW"""
        text = f"Твой тариф успешно продлен"
        buttons = get_back_to_plans()
        return Answer(text=text, buttons=buttons)
    elif description.status == Status.OK and description.action != Action.DOWNGRADE:
        """BUY/UPGRADE"""
        text = f"Желаете ли вы включить атоматическое списывание ?"
        buttons = get_self_buy_buttons()
        return Answer(text=text, buttons=buttons)
    elif description.status == Status.OK and description.action == Action.DOWNGRADE:
        "DOWNGRADE"
        text = "Отлично, твой тариф начнет действовать по истечению текущего"
        buttons = get_back_to_plans()
        return Answer(text=text, buttons=buttons)
    else:
        text = "Упс, что-то пошло не так, попробуй проверить свой баланс и повтори действие"
        buttons = get_back_to_plans()
        return Answer(text=text, buttons=buttons)
