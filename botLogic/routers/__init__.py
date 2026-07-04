__all__ = ("router",)

from aiogram import Router
from .start_handler import router as start_router
from .self_posting import router as self_posting_router
from .common_handlers import router as common_handler_router
from .free_router import router as free_router

router = Router(name=__name__)
router.include_router(start_router)
router.include_router(self_posting_router)
router.include_router(common_handler_router)
router.include_router(free_router)
