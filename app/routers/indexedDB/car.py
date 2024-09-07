from __future__ import annotations
from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from beanie import WriteRules, DeleteRules
from app.models.car import Car as CarDB
from app.utils.random import random_uuid

from app.services.image import resolve_temp_image
from app.utils.time import timestamp_utc_ms

router = APIRouter(tags=["car"])


@router.get("")
async def car_indexedDB():

    cars = await CarDB.find_all().to_list()
    return {
        "version": "abc",
        "lastUpdate": timestamp_utc_ms(),
        "data": [await car.as_json() for car in cars],
    }
