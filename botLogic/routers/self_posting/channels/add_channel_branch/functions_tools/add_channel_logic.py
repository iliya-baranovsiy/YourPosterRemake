from aiogram.types import Chat
from aiogram.enums import ChatType, ChatMemberStatus

from business_logic.services.channels_service.channels_service import ChannelsService
from botLogic.bot_services.bot_instance import bot


class AddTgChannelFacade:
    def __init__(self, forward_from: Chat, tg_id):
        self.tg_id = tg_id
        self.forward_from = forward_from
        self.channel_service = ChannelsService()

    def _is_channel(self) -> bool:
        if self.forward_from:
            return self.forward_from.type == ChatType.CHANNEL
        else:
            return False

    async def _is_exists(self) -> bool:
        exist = await self.channel_service.check_existing(channel_id=self.forward_from.id)
        return exist

    async def _check_membership(self) -> bool:
        try:
            member = await bot.get_chat_member(chat_id=self.forward_from.id, user_id=bot.id)
            return member.status == ChatMemberStatus.ADMINISTRATOR
        except:
            return False

    async def _check_permission(self) -> bool:
        member = await bot.get_chat_member(chat_id=self.forward_from.id, user_id=bot.id)
        return member.can_post_messages

    async def add_channel(self):
        if self._is_channel():
            is_exist = await self._is_exists()
            if not is_exist:
                membership = await self._check_membership()
                if membership:
                    permission = await self._check_permission()
                    if permission:
                        await self.channel_service.add_channel(owner_id=self.tg_id, channel_id=self.forward_from.id,
                                                               channel_name=self.forward_from.title)
                        text = "Канал успешно привязан"
                    else:
                        text = "Добавь боту возможность писать сообщения и попробуй заново"
                else:
                    text = "Бот не является администратором. Сделай его админом и попробуй заново"
            else:
                text = "Этот канал уже привязан"
        else:
            text = "Перешли сообщение из канала"
        return text
