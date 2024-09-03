from __future__ import annotations
from fastapi import APIRouter, UploadFile, File, Path
from app.types.http import Url
from app.models.country import Country
from app.models.country.i18n import CountryName
from .create import router as createRouter
from pydantic import BaseModel, Field, HttpUrl, FilePath
from typing import List, Dict, Any, Optional, Annotated

router = APIRouter(prefix="/country", tags=["country"])

# router.include_router(createRouter)

from app.utils.time import datetime_utc


class CountryCreate(BaseModel):

    name: List[CountryName]
    image_url: Url


@router.get("")
async def get_country():

    # await Country.find_all().update(
    #     {}, {"$set": {"uploaded_at": datetime_utc(), "last_edited": datetime_utc()}}
    # )
    country = await Country.get("66cf23a7d1bd69047ff7d4c8")

    return await country.as_json()


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
    # TODO: en='...' Field 추가
    await Country(name=names, image_url=country.image_url).create()

    return


@router.get("/{name}")
async def create_country(name: Annotated[str, Path()]):
    print(f"{name=}")

    country_name = await CountryName.find_one(CountryName.value == name)
    print(country_name)
    country = await Country.find_one({Country.name: country_name.to_ref()})
    await country.fetch_all_links()
    print(country)
    # existing: CountryName = []
    # for name in country.name:
    #     exists = await CountryName.find_one(CountryName.value == name.value)
    #     if exists:
    #         existing.append(exists)
    # if len(existing) > 0:
    #     return

    # names = [await n.create() for n in country.name]
    # await Country(name=names, image_url=country.image_url).create()
    cnt = await country.as_json()
    return cnt
