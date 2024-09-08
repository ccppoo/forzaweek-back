from fastapi import APIRouter
from .decal import router as decalRouter
from .tuning import router as tuningRouter
from .race_route import router as raceRouteRouter
from .car import router as carRouter


__all__ = ("router",)

router = APIRouter(prefix="/FH5", tags=["FH5"])

router.include_router(decalRouter)
router.include_router(tuningRouter)
router.include_router(raceRouteRouter)
router.include_router(carRouter)
