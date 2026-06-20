__all__ = ("router",)

from aiogram import Router
from .add_channel_handlers import router as add_channel_router

router = Router(name=__name__)
router.include_router(router=add_channel_router)
