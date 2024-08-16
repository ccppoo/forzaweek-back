from fastapi import APIRouter
from .tagging import router as taggingRouter

__all__ = ("router",)

router = APIRouter(prefix="/tagging", tags=["tagging"])

router.include_router(taggingRouter)
