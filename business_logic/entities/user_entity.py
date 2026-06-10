from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from database.payments.options import PaymentOptions


@dataclass
class User:
    tg_id: int
    username: str
    payment_plan: PaymentOptions
    balance: Decimal
    automatic_buy: bool
    end_date: datetime | None = None
    activate_date: datetime | None = None

    @property
    def payment_plan_str(self):
        return self.payment_plan.value
