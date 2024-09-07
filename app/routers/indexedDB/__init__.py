from __future__ import annotations
from fastapi import APIRouter
from fastapi.websockets import WebSocketState
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import json
from pprint import pprint
from datetime import datetime
from bson import ObjectId
from beanie import WriteRules, DeleteRules

from app.models.manufacturer import Manufacturer as ManufacturerDB

from app.services.image import resolve_temp_image
from app.utils.time import timestamp_utc_ms
from .country import router as countryRouter
from .manufacturer import router as manufacturerRouter
from .car import router as carRouter
from .fh5 import router as FH5Router

router = APIRouter(prefix="/db", tags=["indexedDB", "web client"])

router.include_router(countryRouter, prefix="/country")
router.include_router(manufacturerRouter, prefix="/manufacturer")
router.include_router(carRouter, prefix="/car")
router.include_router(FH5Router, prefix="/FH5")
