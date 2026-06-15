from database.payments.options import PaymentOptions, PLAN_INFO
from .options import Action, ActionData
from business_logic.services.user_service import UserService
from .subscription_fabric import SubscriptionFabric
from business_logic.common_options.status_option import Status
from business_logic.entities.payment_plan_entity import DescriptionStatus


class SubscribeService:
    def __init__(self):
        self._user_service = UserService()
        self._fabric = SubscriptionFabric()

    def _get_action(self, current_plan: PaymentOptions, new_plan: PaymentOptions):
        if current_plan == PaymentOptions.STANDART:
            return Action.BUY
        current_priority = PLAN_INFO[current_plan].priority
        new_priority = PLAN_INFO[new_plan].priority

        if new_priority > current_priority:
            return Action.UPGRADE
        elif new_priority < current_priority:
            return Action.DOWNGRADE
        elif new_priority == current_priority:
            return Action.RENEW

    async def get_confirmation_data(self, tg_id: int, new_plan: str) -> ActionData:
        new_plan = PaymentOptions(new_plan)
        user = await self._user_service.get_user(tg_id)
        action = self._get_action(current_plan=user.subscription.payment_plan, new_plan=new_plan)
        fabric_method = self._fabric.create(action=action)
        data = await fabric_method.get_confirmation_text(new_plan=new_plan)
        return data

    async def change_payment_plan(self, new_plan: str, tg_id: int, action: Action) -> DescriptionStatus:
        new_plan = PaymentOptions(new_plan)
        user = await self._user_service.get_user(tg_id)
        fabric_method = self._fabric.create(action)
        if PLAN_INFO[new_plan].price <= user.balance:
            status = await self.fabric_execute(fabric_method=fabric_method, user=user, new_plan=new_plan)
            return DescriptionStatus(status=status, action=action)
        elif action == Action.UPGRADE:
            status = await self.fabric_execute(fabric_method=fabric_method, user=user, new_plan=new_plan)
            return DescriptionStatus(status=status, action=action)
        else:
            return DescriptionStatus(status=Status.BAD, action=action)

    async def fabric_execute(self, fabric_method, user, new_plan):
        try:
            await fabric_method.execute(user=user, new_plan=new_plan)
            return Status.OK
        except Exception as e:
            return Status.BAD
