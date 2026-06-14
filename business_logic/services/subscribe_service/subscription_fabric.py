from decimal import Decimal
from abc import ABC, abstractmethod
from ..subscribe_service.options import Action, ActionData
from database.payments.options import PLAN_INFO, PaymentOptions
from business_logic.entities.user_entity import User


class BaseSubFabric(ABC):
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
        pass


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
