from pydantic import BaseModel
from decimal import Decimal
from datetime import datetime
from ..payments.options import PaymentOptions


class UserDto(BaseModel):
    username: str
    balance: Decimal
    payment_plan: PaymentOptions
    automatic_buy: bool
    end_date: datetime | None
    priority: int
    pending_plan: PaymentOptions
