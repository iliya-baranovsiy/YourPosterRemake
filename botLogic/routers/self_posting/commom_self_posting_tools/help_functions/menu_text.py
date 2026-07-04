from business_logic.entities.user_entity import User


def get_menu_text(user: User) -> str:
    text = (f"👤 <b>Тариф:</b> {user.subscription.payment_plan_str}\n"
            f"📅 <b>Действует по:</b> {user.subscription.end_date}\n"
            f"💰 <b>Баланс:</b> {user.balance}$\n"
            f"Выберите действие ниже.")
    return text
