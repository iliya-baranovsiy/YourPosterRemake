from dataclasses import dataclass
from decimal import Decimal
from .payment_plan_entity import Subscription


@dataclass
class User:
    tg_id: int
    username: str
    balance: Decimal
    automatic_buy: bool
    subscription: Subscription
