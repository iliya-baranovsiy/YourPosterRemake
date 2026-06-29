__all__ = ("router",)

from aiogram import Router
from .channels_settings_menu import router as channels_main_menu_router
from .delete_channel_handler import router as delete_channel_router
from .settings_menu_handler import router as settings_handler_router
from .settings_time_handler import router as time_handler_router
from .settings_switch_handler import router as switch_router
from .settings_theme_handler import router as theme_router
from .change_source_handler import router as change_source_router
from .load_file_handler import router as load_file_router

router = Router(name=__name__)
router.include_router(router=channels_main_menu_router)
router.include_router(router=delete_channel_router)
router.include_router(router=settings_handler_router)
router.include_router(router=theme_router)
router.include_router(router=switch_router)
router.include_router(router=time_handler_router)
router.include_router(router=change_source_router)
router.include_router(router=load_file_router)
