from fastapi import APIRouter
from .decal import router as decalRouter
from .tuning import router as tuningRouter
from .track import router as trackRouter


__all__ = ("router",)

router = APIRouter(prefix="/FH5", tags=["FH5"])

router.include_router(decalRouter)
router.include_router(tuningRouter)
router.include_router(trackRouter)
