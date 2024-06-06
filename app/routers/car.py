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
    CarAbbreviation,
    EngineTypeName,
    DriveTrainTypeName,
)
from app.models.bodyStyle import BodyStyle as BodyStyleDB, BodyStyleName
from app.models.driveTrain import DriveTrain as DriveTrainDB, DriveTrainName
from app.models.engine import Engine as EngineDB, EngineName, EngineDescription
import urllib


router = APIRouter(prefix="/car", tags=["car"])


class Nation(BaseModel):
    name: str
    locale: str


class Car(BaseModel):
    name: str  # CarName
    abbreviation: Optional[str]  # CarAbbreviation
    manufacturer: str  #  Manufacturer
    bodyStyle: str  # BodyStyle
    driveTrainType: str  # FWD, AWD, RWD - 간단한 분류
    driveTrain: Optional[str] = Field(default=None)  # DriveTrain
    engineType: str  # 내연기관, 전기 - 간단한 분류
    engine: Optional[str] = Field(default=None)  # Engine
    year: int
    door: int
    lang: str


class CarGet(BaseModel):
    name: str
    lang: str


@router.get("")
async def get_car(car: CarGet):

    carDB = await CarDB.find_one(
        CarDB.name.lang == car.lang,
        CarDB.name.value == car.name,
        fetch_links=True,
    )

    if carDB:
        carDB: CarDB
        return await carDB.to_json(car.lang)

    return carDB


@router.post("")
async def add_car(car: Car):

    lang = car.lang
    name = car.name

    carDB = await CarDB.find_one(
        CarDB.name.lang == lang,
        CarDB.name.value == name,
        fetch_links=True,
    )

    if carDB:
        return await carDB.to_json(lang)

    carName = await CarName(value=car.name, lang=lang).insert()
    carAbbrev = await CarAbbreviation(
        value=car.abbreviation or car.name, lang=lang
    ).insert()

    # 제조사
    carManufacture = await ManufacturerDB.find_one(
        ManufacturerDB.name.value == car.manufacturer,
        ManufacturerDB.name.lang == car.lang,
        fetch_links=True,
    )

    # if carManufacture:
    # print(f"{carManufacture=}")

    # 바디 스타일
    carBodystyle = await BodyStyleDB.find_one(
        BodyStyleDB.name.value == car.bodyStyle, BodyStyleDB.name.lang == car.lang
    )

    if not carBodystyle:
        bodyStyleName = await BodyStyleName(value=car.bodyStyle, lang=car.lang).insert()
        carBodystyle = await BodyStyleDB(
            name=[bodyStyleName],
        ).insert()

    # 구동방식 이름
    driveTrainTypeName = await DriveTrainTypeName.find_one(
        DriveTrainTypeName.value == car.driveTrainType,
        DriveTrainTypeName.lang == car.lang,
    )
    if not driveTrainTypeName:
        driveTrainTypeName = await DriveTrainTypeName(
            value=car.driveTrainType, lang=car.lang
        ).insert()

    driveTrainDB = None
    # 구동 방식 (세부 종류)
    if car.driveTrain:
        driveTrainDB = await DriveTrainDB.find_one(
            DriveTrainDB.abbreviation == car.driveTrain
        )
        # 이거는 사전에 등록해야하는 정보

    # 엔진 이름
    engineTypeName = await EngineTypeName.find_one(
        EngineTypeName.value == car.engineType,
        EngineTypeName.lang == car.lang,
    )
    if not engineTypeName:
        engineTypeName = await EngineTypeName(
            value=car.engineType, lang=car.lang
        ).insert()

    carEngineDB = None
    # 엔진 (세부 종류)
    if car.engine:
        carEngineDB = await EngineDB.find_one(
            EngineDB.name.value == car.engine, EngineDB.name.lang == car.lang
        )
        # 없으면 사전 등록 ㅇㅇ

    carDB: CarDB = await CarDB(
        name=[carName],
        abbreviation=[carAbbrev],
        manufacturer=carManufacture,
        driveTrainType=[driveTrainTypeName],
        driveTrain=driveTrainDB,
        engineType=[engineTypeName],
        engine=carEngineDB,
        bodyStyle=carBodystyle,
        year=car.year,
        door=car.door,
    ).insert()
    return carDB.model_dump()
