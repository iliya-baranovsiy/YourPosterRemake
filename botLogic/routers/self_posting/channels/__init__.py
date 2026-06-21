__all__ = ("router",)

from aiogram import Router
from .channels_menu import router as channels_menu_router
from .add_channel_branch import router as add_channel_router
from .channel_settings_branch import router as channels_settings_router

router = Router(name=__name__)
router.include_router(router=channels_menu_router)
router.include_router(router=add_channel_router)
router.include_router(router=channels_settings_router)
