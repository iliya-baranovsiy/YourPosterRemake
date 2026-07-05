__all__ = ("router",)

from aiogram import Router
from .deposits_main_menu import router as menu_router
from .stars_deposit import router as stars_deposit_router

router = Router(name=__name__)

router.include_router(router=menu_router)
router.include_router(router=stars_deposit_router)
