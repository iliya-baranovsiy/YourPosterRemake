from decimal import Decimal
from abc import ABC, abstractmethod
from ..subscribe_service.options import Action, ActionData
from database.payments.options import PLAN_INFO, PaymentOptions
from business_logic.entities.user_entity import User
from business_logic.repositories.user_repository import UserRepository
from business_logic.repositories.cache_repository import UserCacheRepository
from datetime import date, timedelta
from exceptions.cash_exception import UserCashException


class BaseSubFabric(ABC):
    def __init__(self):
        self.repo = UserRepository()
        self.cache = UserCacheRepository()

    @abstractmethod
    async def get_confirmation_text(self, new_plan: PaymentOptions):
        pass

    @abstractmethod
    async def execute(self, user: User, new_plan: PaymentOptions):
        pass


class Buy(BaseSubFabric):
    async def get_confirmation_text(self, new_plan):
        text = (f"Уверены ли Вы, что хотите приобрести тариф {new_plan.value}, "
                f"стоимостью {PLAN_INFO[new_plan].price.quantize(Decimal("0.00"))}$ сроком на 31 день ?")
        data = ActionData(text=text, action=Action.BUY)
        return data

    async def execute(self, user, new_plan):
        user.subscription.payment_plan = new_plan
        user.subscription.priority = PLAN_INFO[new_plan].priority
        user.subscription.end_date_row = date.today() + timedelta(days=31)
        user.balance -= PLAN_INFO[new_plan].price
        if user.balance < 0:
            raise UserCashException(user_id=user.tg_id, balance=user.balance)
        else:
            await self.repo.update(user=user, start_date=date.today())
            await self.cache.update_user_cache(user=user)


class Renew(BaseSubFabric):
    async def get_confirmation_text(self, new_plan):
        text = (f"Уверены ли Вы, что хотите продлить тариф {new_plan.value}, "
                f"стоимостью {PLAN_INFO[new_plan].price.quantize(Decimal("0.00"))}$ сроком на 31 день ?")
        data = ActionData(text=text, action=Action.RENEW)
        return data

    async def execute(self, user, new_plan):
        pass


class Upgrade(BaseSubFabric):
    async def get_confirmation_text(self, new_plan):
        text = (f"Уверены ли Вы, что хотите перейти на тариф {new_plan.value}, "
                f"стоимостью {PLAN_INFO[new_plan].price.quantize(Decimal("0.00"))}$ ?")
        data = ActionData(text=text, action=Action.UPGRADE)
        return data

    async def execute(self, user, new_plan):
        pass


class Downgrade(BaseSubFabric):
    async def get_confirmation_text(self, new_plan):
        text = (f"Уверены ли Вы, что хотите перейти на тариф {new_plan.value}, "
                f"стоимостью {PLAN_INFO[new_plan].price.quantize(Decimal("0.00"))}$ он начнет действовать по истечению текущего тарифа?")
        data = ActionData(text=text, action=Action.DOWNGRADE)
        return data

    async def execute(self, user, new_plan):
        pass


class SubscriptionFabric:
    @staticmethod
    def create(action: Action):
        mapping = {
            action.BUY: Buy(),
            Action.RENEW: Renew(),
            Action.UPGRADE: Upgrade(),
            Action.DOWNGRADE: Downgrade(),
        }
        return mapping[action]
