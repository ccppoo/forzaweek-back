from fastapi import APIRouter, UploadFile, File, Query, Depends, Path
from app.models.manufacturer import Manufacturer as ManufacturerDB
from app.models.manufacturer import ManufacturerName

from pydantic import BaseModel, Field
from typing import List, Optional, Annotated
from app.models.country import Country
from app.models.country.i18n import CountryName
from pprint import pprint
from app.models.manufacturer import Manufacturer
from app.types.http import Url

from .create import router as createRouter
from .temp import router as tempRouter

router = APIRouter(prefix="/manufacturer", tags=["manufacturer"])
# router.include_router(createRouter)


class ManufacturerCreate(BaseModel):
    en: str
    origin: str  # str -> find in country document -> Link[Country]
    founded: int
    name: List[ManufacturerName]
    image_url: Url


class ManufacturerQueryParam(BaseModel):
    name: Optional[str] = Query(None, description="name")
    country: Optional[str] = Query(None, description="country")


@router.get("")
async def get_manufacturer():
    manu = await ManufacturerDB.get("66d001e9f2d9ae267ee19172")

    return await manu.as_json()


# @router.get("")
# async def search_manufacturer(
#     query: ManufacturerQueryParam = Depends(),
# ):
#     # {"value": {"$regex": f"^.*{keyword}.*$", "$options": "i"}},
#     # pprint(query)
#     queries = []
#     man_name = None
#     country_name = None
#     country = None
#     if query.name:
#         # queries.append({"name": {"$regex": f"^.*{query.name}.*$", "$options": "i"}})
#         man_name = await ManufacturerName.find_one(
#             {"value": {"$regex": f"^.*{query.name}.*$", "$options": "i"}}
#         )
#         queries.append({ManufacturerDB.name: man_name.to_ref()})
#     if query.country:
#         country_name = await CountryName.find_one(
#             {"value": {"$regex": f"^.*{query.country}.*$", "$options": "i"}}
#         )
#         # print(country_name)
#         if country_name:
#             country = await Country.find_one({Country.name: country_name.to_ref()})
#             if country:
#                 queries.append({ManufacturerDB.origin: country.to_ref()})
#     man = None
#     if queries:
#         man = await ManufacturerDB.find_one(*queries)

#     return man


@router.get("/{name}")
async def get_manufacturer(name: Annotated[str, Path()]):
    man_name = await ManufacturerName.find_one(
        {
            ManufacturerName.value: {
                "$regex": f"{name.replace(' ', '_')}",
                "$options": "i",
            }
        }
    )
    # print(f"{man_name=}")
    if not man_name:
        return

    manufac = await ManufacturerDB.find_one({ManufacturerDB.name: man_name.to_ref()})
    manufac_json = await manufac.as_json()
    return manufac_json


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
