import enum
from dataclasses import dataclass
from decimal import Decimal


class PaymentOptions(str, enum.Enum):
    STANDART = "STANDART"
    PRO = "PRO"
    VIP = "VIP"


@dataclass(frozen=True)
class PlanInfo:
    priority: int
    price: Decimal


PLAN_INFO = {
    PaymentOptions.STANDART: PlanInfo(
        priority=0,
        price=Decimal(0.0)
    ),
    PaymentOptions.PRO: PlanInfo(
        priority=2,
        price=Decimal(2.99)
    ),
    PaymentOptions.VIP: PlanInfo(
        priority=1,
        price=Decimal(5.99)
    )
}
