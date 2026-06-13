__all__ = ("router",)

from aiogram import Router
from .pricing_plans_menu import router as pricing_plans_router

router = Router(name=__name__)
router.include_router(pricing_plans_router)
