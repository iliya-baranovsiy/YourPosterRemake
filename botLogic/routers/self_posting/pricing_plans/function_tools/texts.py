from business_logic.entities.user_entity import User


def get_pricing_plan_text(user: User) -> str:
    text = (f"<b>Тариф:</b> {user.subscription.payment_plan_str}\n"
            f"<b>Действует по:</b> {user.subscription.end_date}\n"
            f"<b>Баланс:</b> {user.balance}")
    return text


def get_un_success_text() -> str:
    text = "Упс, что-то пошло не так, проверь средства на балансе и попробуй заново"
    return text
