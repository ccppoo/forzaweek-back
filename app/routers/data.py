from __future__ import annotations
from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel, Field, HttpUrl, FilePath
from typing import List, Dict, Any, Optional
from pprint import pprint
from datetime import datetime
from app.configs import awsSettings, runtimeSettings, cfSettings
from app.models.nation import Nation as NationDB
from app.models.manufacturer import Manufacturer as ManufacturerDB
from app.models.car import Car as CarDB
from fastapi import FastAPI, File, UploadFile

router = APIRouter(prefix="/data", tags=["data"])


class DataStatus(BaseModel):
    nation: int
    manufacturer: int
    car: int


@router.get("/status")
async def get_data_status() -> DataStatus:

    naiton_count = await NationDB.count()
    manufac_count = await ManufacturerDB.count()
    car_count = await CarDB.count()

    dataStatus = DataStatus(
        nation=naiton_count, manufacturer=manufac_count, car=car_count
    )
    return dataStatus
