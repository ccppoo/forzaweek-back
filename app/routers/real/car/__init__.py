from __future__ import annotations
from fastapi import APIRouter
from .create import router as createRouter
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Union
from app.models.car import (
    Car as Car_Real,
    CarName,
)
from beanie import DeleteRules, WriteRules

router = APIRouter(prefix="/car", tags=["car", "real"])


# # image_urls: List[Url]
# # first_image: Optional[Url]

# alias: List[Link[CarAlias]] = Field([])

# manufacturer: Link[Manufacturer]  # 국가 추출해서

# production_year: int = Field(ge=1900)
# engine_type: str
# body_style: List[str] = Field([])
# door: int = Field(ge=0)


@router.get("")
async def get_real_car():
    # Car_Real
    car_real = await Car_Real.get("66d69c5fa368e84afdbb633d")
    return await car_real.as_json()


@router.post("")
async def add_real_car(real_car: Car_Real):
    # Car_Real
    car_created = await real_car.insert(link_rule=WriteRules.WRITE)
    return car_created.model_dump()
