from fastapi import APIRouter
from .xbox import router as xboxAuthRouter

__all__ = ("router",)

router = APIRouter(prefix="/oauth", tags=["auth"])

router.include_router(xboxAuthRouter)
