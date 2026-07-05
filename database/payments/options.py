import enum
from dataclasses import dataclass
from decimal import Decimal


class PaymentOptions(str, enum.Enum):
    STANDART = "STANDART"
    PRO = "PRO"
    VIP = "VIP"


class PaymentStatus(str, enum.Enum):
    SUCCESS = "SUCCESS"
    SETBACK = "SETBACK"


@dataclass(frozen=True)
class PlanInfo:
    priority: int
    price: Decimal
    channels_count: int
    posts_count: int
    file_load: bool
    ai_load: bool


PLAN_INFO = {
    PaymentOptions.STANDART: PlanInfo(
        priority=0,
        price=Decimal(0.0),
        channels_count=1,
        posts_count=2,
        file_load=False,
        ai_load=False
    ),
    PaymentOptions.PRO: PlanInfo(
        priority=1,
        price=Decimal(2.99),
        channels_count=2,
        posts_count=4,
        file_load=True,
        ai_load=False
    ),
    PaymentOptions.VIP: PlanInfo(
        priority=2,
        price=Decimal(5.99),
        channels_count=4,
        posts_count=5,
        file_load=True,
        ai_load=True
    )
}
