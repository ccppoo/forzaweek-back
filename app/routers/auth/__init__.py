from fastapi import APIRouter
from .oauth import router as oAuthRouter

__all__ = ("router",)

router = APIRouter(prefix="/auth", tags=["auth"])

router.include_router(oAuthRouter)
