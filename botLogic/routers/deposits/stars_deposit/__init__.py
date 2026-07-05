__all__ = ("router",)

from aiogram import Router
from .stars_deposit_handler import router as stars_router

router = Router(name=__name__)
router.include_router(router=stars_router)
