from fastapi import APIRouter
from .decal import decalRouter
from .tuning import tuningRouter

__all__ = ("router",)

router = APIRouter(prefix="/fh5", tags=["fh5"])

router.include_router(decalRouter)
router.include_router(tuningRouter)
