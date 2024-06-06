from __future__ import annotations
from fastapi import APIRouter, UploadFile, File
from fastapi.websockets import WebSocketState
from pydantic import BaseModel, Field
import anyio
from typing import List, Dict, Any, Optional
import asyncio
import json
from pprint import pprint
from datetime import datetime

from app.configs import awsSettings
from app.models.manufacturer import (
    Manufacturer as ManufacturerDB,
    ManufacturerDescription,
    ManufacturerName,
)
from app.models.nation import Nation as NationDB, NationName
import botocore
import urllib


router = APIRouter(prefix="/manufacturer", tags=["image"])


class Nation(BaseModel):
    name: str
    locale: str


class Manufacturer(BaseModel):
    name: str
    founded: int
    description: str
    nation: str
    lang: str


class ManufacturerGet(BaseModel):
    name: str
    founded: int
    description: str
    nation: str
    lang: str


@router.get("")
async def get_manufacturer(manufacturer: ManufacturerGet):

    man = await ManufacturerDB.find_one(
        ManufacturerDB.name.lang == manufacturer.lang,
        ManufacturerDB.name.value == manufacturer.name,
        fetch_links=True,
    )

    if man:
        man: ManufacturerDB
        return man.to_json(manufacturer.lang)

    return man


@router.post("")
async def add_manufacturer(manufacturer: Manufacturer):

    lang = manufacturer.lang
    name = manufacturer.name
    nation = manufacturer.nation

    manfuc = await ManufacturerDB.find_one(
        ManufacturerDB.name.lang == lang,
        ManufacturerDB.name.value == name,
        fetch_links=True,
    )

    if manfuc:
        return

    Mname = await ManufacturerName(value=name, lang=lang).insert()
    Mdescript = await ManufacturerDescription(
        value=manufacturer.description, lang=lang
    ).insert()

    nationDB = await NationDB.find_one(
        NationDB.name.lang == lang, NationDB.name.value == nation, fetch_links=True
    )
    if not nationDB:
        nationName = await NationName(value=nation, lang=lang).insert()
        # NOTE: 이미 존재하는 국가의 경우 프런트에서 영어로 이미 데이터에 있는 국가 그대로 보여주고 선택하도록 해야됨
        nationDB = await NationDB(name=[nationName]).insert()

    manufacturerDB: ManufacturerDB = await ManufacturerDB(
        name=[Mname],
        founded=manufacturer.founded,
        description=[Mdescript],
        origin=nationDB,
    ).insert()
    return manufacturerDB.model_dump()
