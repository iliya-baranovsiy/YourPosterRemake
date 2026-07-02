from datetime import timedelta, date

from business_logic.services.user_service import UserService
from business_logic.services.channels_service.channels_service import ChannelsService
from business_logic.entities.user_entity import User
from database.payments.options import PaymentOptions, PLAN_INFO
from database.backgroundt_tasks_db.orm import BackGroundTasksORM


class CheckPaymentPlan:
    def __init__(self):
        self.user_service = UserService()
        self.channel_service = ChannelsService()
        self.orm = BackGroundTasksORM()

    async def update_plan(self):
        try:
            ids = await self._get_ids()
            for id_ in ids:
                user = await self.user_service.get_user(tg_id=id_)
                if user.automatic_buy:
                    balance = user.balance - PLAN_INFO[user.subscription.payment_plan].price
                    if balance >= 0:
                        user.balance = balance
                        user.subscription.end_date_row = date.today() + timedelta(days=31)
                        await self.user_service.update_user(user)
                    else:
                        await self._downgrade_payment(id_=id_, user=user)
                else:
                    await self._downgrade_payment(id_=id_, user=user)
        except:
            pass

    async def _get_ids(self) -> set:
        data = await self.orm.get_payments_ids(today=date.today())
        return set(data)

    async def _downgrade_payment(self, id_: int, user: User):
        user.subscription.payment_plan = PaymentOptions.STANDART
        user.subscription.end_date_row = None
        await self.user_service.update_user(user=user)
        user_channels = await self.channel_service.get_channels(owner_id=id_)
        to_delete = user_channels.channels_count - PLAN_INFO[PaymentOptions.STANDART].channels_count
        channels = user_channels.channels[:to_delete]
        if to_delete > 0:
            for channel in channels:
                await self.channel_service.delete_channel(owner_id=id_,
                                                          channel_id=channel.channel_id)
