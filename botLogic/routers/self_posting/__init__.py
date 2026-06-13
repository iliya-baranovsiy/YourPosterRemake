__all__ = ("router",)

from aiogram import Router
from .self_posting_menu import router as self_posting_menu_router

router = Router(name=__name__)
router.include_router(self_posting_menu_router)
