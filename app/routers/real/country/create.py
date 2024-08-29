from __future__ import annotations
from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel, Field, HttpUrl, FilePath
from typing import List, Dict, Any, Optional
from pprint import pprint
from datetime import datetime
from app.configs import awsSettings, runtimeSettings, cfSettings
from app.models.country import Country
from app.models.country.i18n import CountryName
from app.models.manufacturer import Manufacturer
from beanie import WriteRules, DeleteRules
from fastapi import FastAPI, File, UploadFile
import pathlib
import os
from app.cloud import client_r2
from app.services.dbState import updateDBState
from app.types.http import Url


__all__ = ("create_country",)

router = APIRouter(prefix="/create")


class CountryCreate(BaseModel):

    name: List[CountryName]
    image_url: Url


@router.post("")
async def create_country(country: CountryCreate):

    existing: CountryName = []
    for name in country.name:
        exists = await CountryName.find_one(CountryName.value == name.value)
        if exists:
            existing.append(exists)
    if len(existing) > 0:
        return

    names = [await n.create() for n in country.name]
    await Country(name=names, image_url=country.image_url).create()

    return


@router.post("/test")
async def create_country_test():
    existing: CountryName = []
    for name in country.name:
        exists = await CountryName.find_one(CountryName.value == name.value)
        if exists:
            existing.append(exists)
    name_id = [str(e.id) for e in existing]
    country = await Country.find_one({"name": {"$elemMatch": {"$in": name_id}}})
    return
