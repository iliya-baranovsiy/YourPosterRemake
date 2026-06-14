from decimal import Decimal


class UserCashException(Exception):
    def __init__(self, balance: Decimal, user_id: int):
        self.balance = balance
        self.user_id = user_id

    def __str__(self):
        return f"Недопустимое значение, баланс пользователя (id: {self.user_id}) не может быть отрицательным {self.balance}"
