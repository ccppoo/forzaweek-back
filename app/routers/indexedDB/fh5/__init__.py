from fastapi import APIRouter

from .car import router as carRouter
from .race_route import router as raceRouteRouter

router = APIRouter()

router.include_router(carRouter, prefix="/car")
router.include_router(raceRouteRouter, prefix="/raceroute")
