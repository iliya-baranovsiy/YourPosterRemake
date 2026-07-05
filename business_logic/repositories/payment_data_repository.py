from database.payments.orm import PaymentDataORM
from database.payments.options import PaymentStatus


class PaymentRepository:
    def __init__(self):
        self.orm = PaymentDataORM()

    async def insert_payment_data(self, user_id: int, amount: int, telegram_charge_id: str, payload: str,
                                  status: PaymentStatus):
        await self.orm.insert_pyment(user_id=user_id,
                                     amount=amount,
                                     telegram_charge_id=telegram_charge_id,
                                     payload=payload,
                                     status=status, )

    async def check_payment_existing(self, telegram_charge_id: str) -> bool:
        data = await self.orm.check_existing_payment_data(telegram_charge_id=telegram_charge_id)
        return data

    async def get_payment_status(self, user_id: int, telegram_charge_id: str) -> PaymentStatus:
        data = await self.orm.get_payment_data(user_id=user_id, telegram_charge_id=telegram_charge_id)
        return data
