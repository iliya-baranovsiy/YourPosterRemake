from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from database.payments.options import PaymentOptions


@dataclass
class User:
    tg_id: int
    username: str
    payment_plan: PaymentOptions | str
    balance: Decimal
    automatic_buy: bool
    end_date_row: datetime | None

    # activate_date_row: datetime | None = None

    @property
    def payment_plan_str(self):
        return self.payment_plan.value

    @property
    def end_date(self):
        if self.end_date_row:
            return self.end_date_row
        return "Бессрочно"
