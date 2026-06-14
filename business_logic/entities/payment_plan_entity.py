from dataclasses import dataclass
from datetime import date
from database.payments.options import PaymentOptions


@dataclass
class Subscription:
    payment_plan: PaymentOptions
    end_date_row: date | None
    priority: int
    pending_plan: PaymentOptions

    @property
    def payment_plan_str(self):
        return self.payment_plan.value

    @property
    def end_date(self):
        if self.end_date_row:
            return self.end_date_row
        return "Бессрочно"
