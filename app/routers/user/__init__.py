from fastapi import APIRouter
from .profile import router as profileRouter
from .me import router as meRouter

__all__ = ("router",)

router = APIRouter(prefix="/user", tags=["auth", "user"])

router.include_router(profileRouter)
router.include_router(meRouter)
