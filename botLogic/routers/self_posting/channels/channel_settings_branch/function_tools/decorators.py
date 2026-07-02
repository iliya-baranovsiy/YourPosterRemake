from functools import wraps
from aiogram.types import Message, CallbackQuery

from business_logic.services.user_service import UserService
from database.payments.options import PaymentOptions
from botLogic.common_bot_tools.keyboards.main_menu_kb import get_main_menu_kb


def required_plan():
    def decorator(handler):
        @wraps(handler)
        async def wrapper(event, *args, **kwargs):
            user = await UserService().get_user(event.from_user.id)
            if user.subscription.payment_plan == PaymentOptions.STANDART:
                buttons = get_main_menu_kb()
                try:
                    await event.message.edit_text("У тебя нет доступа к этой функции")
                except:
                    await event.message.answer("У тебя нет доступа к этой функции")
                await event.message.answer("Главное меню", reply_markup=buttons)
                return
            else:
                return await handler(event, *args, **kwargs)

        return wrapper

    return decorator
