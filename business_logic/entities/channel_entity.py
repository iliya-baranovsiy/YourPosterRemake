from dataclasses import dataclass
from database.payments.options import PaymentOptions
from business_logic.services.channels_service.options.options import Resource, PostTheme


@dataclass
class BaseChannelInfo:
    channel_id: int
    channel_name: str


@dataclass
class UserChannelsInfo:
    tg_id: int
    payment_plan: PaymentOptions
    channels_count: int
    channels: list[BaseChannelInfo]

    @property
    def payment_plan_str(self):
        return self.payment_plan.value


@dataclass
class ChannelSettings:
    channel_id: int
    owner_id: int
    channel_name: str
    posts_available_count: int
    posts_count: int
    theme: PostTheme
    time: list
    posting_is_active: bool
    resource: Resource
