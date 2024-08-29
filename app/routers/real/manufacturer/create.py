from __future__ import annotations
from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel, Field, HttpUrl, FilePath
from typing import List, Dict, Any, Optional
from pprint import pprint
from datetime import datetime
from app.configs import awsSettings, runtimeSettings, cfSettings
from app.models.manufacturer import Manufacturer
from app.models.manufacturer.i18n import ManufacturerName
from app.models.country import Country

from beanie import WriteRules, DeleteRules
from fastapi import FastAPI, File, UploadFile
import pathlib
import os
from app.cloud import client_r2
from app.services.dbState import updateDBState
from app.types.http import Url


__all__ = ("create_country",)

router = APIRouter(prefix="/create")

# # image_url
# name: List[Link[ManufacturerName]] = Field([])
# alias: List[Link[ManufacturerAlias]] = Field([])
# en: str


# founded: int = Field(ge=1000, le=9999)
# origin: Link[Country]
class ManufacturerCreate(BaseModel):
    en: str
    origin: str  # str -> find in country document -> Link[Country]
    founded: int
    name: List[ManufacturerName]
    image_url: Url


@router.post("")
async def create_country(manufacturer: ManufacturerCreate):

    pprint(manufacturer)
    existing: ManufacturerName = []
    for name in manufacturer.name:
        exists = await ManufacturerName.find_one(ManufacturerName.value == name.value)
        if exists:
            existing.append(exists)
    if len(existing) > 0:
        return
    origin = await Country.find_one(Country.en == manufacturer.origin)
    if not origin:
        return
    names = [await n.create() for n in manufacturer.name]
    await Manufacturer(
        name=names,
        image_url=manufacturer.image_url,
        founded=manufacturer.founded,
        origin=origin,
        en=manufacturer.en,
    ).create()

    return


@router.post("/test")
async def create_country_test():
    existing: ManufacturerName = []
    for name in country.name:
        exists = await ManufacturerName.find_one(ManufacturerName.value == name.value)
        if exists:
            existing.append(exists)
    name_id = [str(e.id) for e in existing]
    country = await Manufacturer.find_one({"name": {"$elemMatch": {"$in": name_id}}})
    return
