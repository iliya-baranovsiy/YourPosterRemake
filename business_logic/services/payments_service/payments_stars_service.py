from decimal import Decimal
from business_logic.repositories.payment_data_repository import PaymentRepository
from business_logic.services.user_service import UserService
from database.payments.options import PaymentStatus
from business_logic.common_options.status_option import Status


class PaymentStarsService:
    def __init__(self):
        self.repo = PaymentRepository()
        self.user_service = UserService()

    async def pay(self, user_id: int, telegram_charge_id: str, amount: int, payload: str):
        exists = await self.repo.check_payment_existing(telegram_charge_id=telegram_charge_id)
        if exists:
            pass
        else:
            try:
                user = await self.user_service.get_user(tg_id=user_id)
                user.balance += Decimal(amount) * Decimal("0.0239")
                await self.user_service.update_user(user)
                await self.repo.insert_payment_data(user_id=user_id, amount=amount,
                                                    telegram_charge_id=telegram_charge_id, payload=payload,
                                                    status=PaymentStatus.SUCCESS)
                return Status.OK
            except:
                await self.repo.insert_payment_data(user_id=user_id, amount=amount,
                                                    telegram_charge_id=telegram_charge_id, payload=payload,
                                                    status=PaymentStatus.SETBACK)
                return Status.BAD
