__all__ = ("router",)

from aiogram import Router
from .self_posting_menu import router as self_posting_menu_router
from .pricing_plans import router as pricing_plans_router
from .channels import router as channels_router

router = Router(name=__name__)
router.include_router(self_posting_menu_router)
router.include_router(pricing_plans_router)
router.include_router(channels_router)
