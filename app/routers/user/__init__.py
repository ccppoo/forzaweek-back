from fastapi import APIRouter
from .profile import router as profileRouter

__all__ = ("router",)

router = APIRouter(prefix="/user", tags=["auth", "user"])

router.include_router(profileRouter)
