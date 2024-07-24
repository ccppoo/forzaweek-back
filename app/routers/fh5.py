from fastapi import APIRouter
from .decal.fh5 import decalRouter
from .tuning.fh5 import tuningRouter
from .track.fh5 import router as trackRouter

__all__ = ("router",)

router = APIRouter(prefix="/FH5", tags=["FH5"])

router.include_router(decalRouter)
router.include_router(tuningRouter)
router.include_router(trackRouter)
