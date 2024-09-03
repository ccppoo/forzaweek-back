from fastapi import APIRouter

from .car import router as carRouter

router = APIRouter()

router.include_router(carRouter, prefix="/car")
