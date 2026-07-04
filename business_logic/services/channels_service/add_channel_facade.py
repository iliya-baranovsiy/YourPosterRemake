from aiogram.types import Chat
from aiogram.enums import ChatType, ChatMemberStatus

from .channels_service import ChannelsService
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
                        text = "✅ Канал успешно привязан."
                    else:
                        text = (
                            "⚠️ Боту не хватает прав для публикации сообщений.\n\n"
                            "Выдайте ему разрешение на отправку сообщений и повторите попытку."
                        )
                else:
                    text = ("⚠️ Бот не является администратором канала.\n\n"
                            "Добавьте его в администраторы и повторите попытку.")
            else:
                text = "ℹ️ Этот канал уже привязан."
        else:
            text = "📢 Пожалуйста перешлите любой пост из канала, который хотите подключить."
        return text
