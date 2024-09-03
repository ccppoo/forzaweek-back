from __future__ import annotations
from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import json
from pprint import pprint
from datetime import datetime
from bson import ObjectId
from beanie import WriteRules, DeleteRules


from app.models.car import (
    Car as CarDB,
    CarName,
)

from app.models.car import Car as CarDB
from app.models.manufacturer import Manufacturer as ManufacturerDB
from app.models.country import Country as CountryDB
from app.utils.random import random_uuid

from app.services.image import resolve_temp_image
from app.utils.time import timestamp_utc_ms

router = APIRouter(tags=["country"])


@router.get("")
async def country_indexedDB():

    countries = await CountryDB.find_all().to_list()
    return {
        "version": "abc",
        "lastUpdate": timestamp_utc_ms(),
        "data": [await cntry.as_json() for cntry in countries],
    }
