from dataclasses import dataclass
from datetime import date, datetime
from database.payments.options import PaymentOptions
from ..common_options.status_option import Status
from ..services.subscribe_service.options import Action


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
            format_date = datetime.strptime(str(self.end_date_row), "%Y-%m-%d").strftime("%d.%m.%Y")
            return format_date
        return "Бессрочно"


@dataclass
class DescriptionStatus:
    status: Status
    action: Action
