from __future__ import annotations
from fastapi import APIRouter
from pydantic import BaseModel, Field
import asyncio
from typing import List, Dict, Any, Optional, Union
from pprint import pprint
from bson import ObjectId
from beanie import DeleteRules, WriteRules

from app.models.manufacturer import (
    Manufacturer as ManufacturerDB,
)
from app.models.FH5.car import Car as Car_FH5
from app.utils.random import random_uuid
from app.services.image import resolve_temp_image
from app.types.http import Url
from app.models.FH5.components.car_details import CarBaseStat

router = APIRouter(prefix="/car", tags=["car"])


class CarShortName(BaseModel):
    pass  # temp


class Nation(BaseModel):
    name: str
    locale: str


class CarGet(BaseModel):
    name: str
    lang: str


@router.get("")
async def get_car():
    car = await Car_FH5.get("66d69c63a368e84afdbb633f")
    _car = await car.as_json()
    return _car


@router.post("")
async def add_car(new_fh5_car: Car_FH5):

    print(new_fh5_car)
    car_fh5 = await new_fh5_car.insert(link_rule=WriteRules.WRITE)
    return car_fh5.model_dump()


@router.post("/edit/{itemID}")
async def update_manufacturer(itemID: str):

    return 200


@router.delete("/{itemID}")
async def delete_car(itemID: str):
    car: Car_FH5 = await Car_FH5.get(itemID, fetch_links=True)
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
    _carDB = await Car_FH5.get(itemID, fetch_links=True)

    if not _carDB:
        return

    carDB = await _carDB.to_json_edit()

    return carDB
