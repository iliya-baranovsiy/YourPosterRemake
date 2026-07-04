from functools import wraps
from ..keyboards.main_menu_kb import get_main_menu_kb


def save_work():
    def decorator(handler):
        @wraps(handler)
        async def wrapper(event, *args, **kwargs):
            try:
                return await handler(event, *args, **kwargs)
            except:
                buttons = get_main_menu_kb()
                try:
                    await event.message.edit_text("Упс, что-то пошло не так")
                except:
                    await event.answer("Упс, что-то пошло не так")
                try:
                    await event.message.answer("Главное меню", reply_markup=buttons)
                except:
                    await event.answer("Главное меню", reply_markup=buttons)

        return wrapper

    return decorator
