__all__ = ("router",)

from aiogram import Router
from .channels_menu import router as channels_menu_router

router = Router(name=__name__)
router.include_router(router=channels_menu_router)
