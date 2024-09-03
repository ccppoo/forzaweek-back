from __future__ import annotations
from fastapi import APIRouter
from pydantic import BaseModel, Field
import asyncio
from typing import List, Dict, Any, Optional, Union
from pprint import pprint
from bson import ObjectId
from beanie import DeleteRules

from app.models.manufacturer import (
    Manufacturer as ManufacturerDB,
)
from app.models.car import (
    Car as CarDB,
    CarName,
)
from app.utils.random import random_uuid
from app.services.image import resolve_temp_image

router = APIRouter(prefix="/car", tags=["car"])


class CarShortName(BaseModel):
    pass  # temp


class Nation(BaseModel):
    name: str
    locale: str


class CarGet(BaseModel):
    name: str
    lang: str


class CarCreate(BaseModel):

    manufacturer: str  # Object ID

    image_urls: List[str] = Field([])
    first_image: Optional[str]

    production_year: int = Field(ge=1900, le=2560)
    engine_type: str
    body_style: str
    door: int = Field(ge=0)

    name: List[CarName]


@router.get("")
async def get_all_cars():

    cars = await CarDB.find_all().to_list()
    [await car.fetch_all_links() for car in cars]

    a = [await car.to_json_all_lang() for car in cars]
    return a


@router.post("")
async def add_real_car(real_car: CarCreate):
    return real_car


@router.post("/edit/{itemID}")
async def update_manufacturer(itemID: str):

    return 200


@router.delete("/{itemID}")
async def delete_car(itemID: str):
    car: CarDB = await CarDB.get(itemID, fetch_links=True)
    if not car:
        return

    name_delete = [
        *[cn.delete() for cn in car.name],
        *[cn.delete() for cn in car.short_name],
    ]
    await asyncio.gather(*name_delete)
    await car.delete(link_rule=DeleteRules.DO_NOTHING)

    return 200


@router.get("/edit/{itemID}")
async def get_car_for_edit(itemID: str):
    _carDB = await CarDB.get(itemID, fetch_links=True)

    if not _carDB:
        return

    carDB = await _carDB.to_json_edit()

    return carDB
