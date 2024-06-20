from __future__ import annotations
from fastapi import APIRouter
from fastapi.websockets import WebSocketState
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import json
from pprint import pprint
from datetime import datetime

from app.models.manufacturer import (
    Manufacturer as ManufacturerDB,
    ManufacturerDescription,
    ManufacturerName,
)
from app.models.nation import Nation as NationDB, NationName
from app.models.car import (
    Car as CarDB,
    CarName,
    CarShortName,
)
from app.models.component.fh5 import FH5_meta

from app.models.bodyStyle import BodyStyle as BodyStyleDB, BodyStyleName
from app.models.driveTrain import DriveTrain as DriveTrainDB, DriveTrainName
from app.models.engine import Engine as EngineDB, EngineName, EngineDescription
from app.utils.random import random_uuid
import asyncio

from app.services.image import resolve_temp_image

router = APIRouter(prefix="/car", tags=["car"])


class Nation(BaseModel):
    name: str
    locale: str


class CarGet(BaseModel):
    name: str
    lang: str


class CarCreate(BaseModel):

    manufacturer: str

    imageURLs: List[str]
    firstImage: Optional[str]

    production_year: int = Field(ge=1900, le=2560)
    engineType: str
    bodyStyle: str
    door: int = Field(ge=0)

    name_en: str
    name: List[CarName]

    short_name_en: str
    short_name: List[CarShortName]

    fh5_meta: FH5_meta


@router.get("")
async def get_all_cars():

    cars = await CarDB.find_all().to_list()
    [await car.fetch_all_links() for car in cars]

    a = [await car.to_json_all_lang() for car in cars]
    return a


@router.post("")
async def add_car(car: CarCreate):

    carDB = await CarDB.find_one(
        CarDB.name_en == car.name_en,
        fetch_links=True,
    )

    # 1. 이미 존재하는 차
    if carDB:
        return
    # 2. 제조사 확인
    manufacturer = await ManufacturerDB.get(car.manufacturer)

    if not manufacturer:
        return

    # 3. 새로 올라온 사진 저장
    if car.firstImage not in car.imageURLs:
        return
    first_img_idx = car.imageURLs.index(car.firstImage)

    # TODO: asyncio 아니면 병렬로 수정한 후 바꿀것
    uploaded_images = []
    for img in car.imageURLs:
        random_name = random_uuid(replace_dash="")
        httpUrl = resolve_temp_image("car", img, random_name, car.short_name_en)
        uploaded_images.append(httpUrl)

    first_image_url = uploaded_images[first_img_idx]

    # 4. 이름 저장
    await asyncio.gather(
        *[n.insert() for n in car.name], *[sn.insert() for sn in car.short_name]
    )

    carDB: CarDB = await CarDB(
        manufacturer=manufacturer,
        images=uploaded_images,
        first_image=first_image_url,
        body_style=car.bodyStyle,
        door=car.door,
        engine_type=car.engineType,
        name_en=car.name_en,
        name=car.name,
        short_name_en=car.short_name_en,
        short_name=car.short_name,
        production_year=car.production_year,
        fh5_meta=car.fh5_meta,
    ).insert()

    return carDB.model_dump()
