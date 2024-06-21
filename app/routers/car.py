from __future__ import annotations
from fastapi import APIRouter
from fastapi.websockets import WebSocketState
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import json
from pprint import pprint
from datetime import datetime
from bson import ObjectId

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


class CarEdit(BaseModel):
    id: str
    manufacturer: str

    imageURLs: List[str]
    firstImage: str

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

    _new_ObjectID = ObjectId()

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
        httpUrl = resolve_temp_image("car", img, random_name, str(_new_ObjectID))
        uploaded_images.append(httpUrl)

    first_image_url = uploaded_images[first_img_idx]

    # 4. 이름 저장
    await asyncio.gather(
        *[n.insert() for n in car.name], *[sn.insert() for sn in car.short_name]
    )

    carDB: CarDB = await CarDB(
        id=_new_ObjectID,
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


@router.post("/edit/{itemID}")
async def update_manufacturer(itemID: str, car: CarEdit):
    assert itemID == car.id

    car_old = await CarDB.get(car.id, fetch_links=True)

    # return
    NAME_EN = car.name_en
    SHORT_NAME_EN = car.short_name_en

    NEW_IMAGE = any([img for img in car.imageURLs if not img.startswith("https")])
    NEW_MANUFACTURER = car.manufacturer != car_old.manufacturer

    if not car_old:
        return 403

    # 1. 이미지 변경
    # NOTE: 이미지 수정 안했을 경우 기존 이미지 URL인 `https~`이므로 수정하지 않는다.
    # NOTE: 이미지는 str[] 이므로 새로운 이미지만 있을 경우 수정하고 업데이트한다
    print(f"{NEW_IMAGE=}")
    if NEW_IMAGE:
        # resolve new image
        for new_img in NEW_IMAGE:
            random_name = random_uuid(replace_dash="")
            httpUrl = resolve_temp_image("car", new_img, random_name, car.short_name_en)
            # uploaded_images.append(httpUrl)
        pass
        # remove old image

    # 2. 제조사
    new_manufacturer = None
    if NEW_MANUFACTURER:
        new_manufacturer = await ManufacturerDB.get(car.manufacturer)

    # 3. name, short name
    names: List[CarName] = CarName.RIGHT_JOIN(left=car_old.name, right=car.name)
    old_names: List[CarName] = CarName.LEFT_ONLY(left=car_old.name, right=car.name)

    short_names: List[CarShortName] = CarShortName.RIGHT_JOIN(
        left=car_old.short_name, right=car.short_name
    )
    old_short_name: List[CarShortName] = CarShortName.LEFT_ONLY(
        left=car_old.short_name, right=car.short_name
    )

    name_jobs = [
        *[n.insert() for n in names if not n.id],
        *[n.insert() for n in short_names if not n.id],
    ]
    # print(f"{name_jobs=}")
    if name_jobs:
        await asyncio.gather(*name_jobs)

    # 4. body style, engine type, doors, 출시연도
    car_old.body_style = car.bodyStyle
    car_old.engine_type = car.engineType
    car_old.door = car.door
    car_old.production_year = car.production_year

    # 5. Forza Horizon 5 Meta
    car_old.fh5_meta = car.fh5_meta

    # 6. DB에 저장
    car_old.name = names
    car_old.name_en = NAME_EN
    car_old.short_name = short_names
    car_old.short_name_en = SHORT_NAME_EN

    if new_manufacturer:
        car_old.manufacturer = new_manufacturer

    # NOTE: 이미지의 경우 이름은 그대로, 버킷에 있는 파일만 바뀌므로 업데이트 안함
    await car_old.save_changes()

    # 안쓰는 i18n 삭제
    old_name_jobs = [
        *[name.delete() for name in old_names],
        *[sname.delete() for sname in old_short_name],
    ]
    if old_name_jobs:
        await asyncio.gather(*old_name_jobs)

    return 200


@router.get("/edit/{itemID}")
async def get_car_for_edit(itemID: str):
    _carDB = await CarDB.get(itemID, fetch_links=False)

    if not _carDB:
        return

    carDB = await _carDB.to_json_edit()

    return carDB
