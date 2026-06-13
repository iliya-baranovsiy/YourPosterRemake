from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from database.payments.options import PaymentOptions
from .payment_plan_entity import Subscription


@dataclass
class User:
    tg_id: int
    username: str
    balance: Decimal
    automatic_buy: bool
    subscription: Subscription
