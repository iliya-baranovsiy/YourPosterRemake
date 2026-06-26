from pydantic import BaseModel
from business_logic.services.channels_service.options.options import Resource, PostTheme


class ChannelSettingsDto(BaseModel):
    post_count: int
    post_theme: PostTheme
    posts_resource: Resource
    is_active_posting: bool
    channel_name: str
    posts_times: list
