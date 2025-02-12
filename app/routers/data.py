from __future__ import annotations
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from pprint import pprint

from app.models.country import Country
from app.models.manufacturer import Manufacturer as ManufacturerDB
from app.models.car import Car as CarDB
from app.models.tag import TagItem as TagDB

# from app.models.tag import TagItemCategory as TagCategoryDB
from app.models.FH5.decal import Decal as Decal_FH5
from app.models.FH5.tuning import Tuning as Tuning_FH5

# from app.models.decal import Decal as DecalDB
# from app.models.tuning import Tuning as TuningDB

router = APIRouter(prefix="/data", tags=["data"])


class DataStatus(BaseModel):
    nation: int
    manufacturer: int
    car: int
    decal: int
    tag: int
    tagkind: int
    tuning: int


@router.get("/status")
async def get_data_status() -> DataStatus:

    naiton_count = await Country.count()
    manufac_count = await ManufacturerDB.count()
    car_count = await CarDB.count()
    tag_count = await TagDB.count()
    decal_count = await Decal_FH5.count()
    # tagkind_count = await TagCategoryDB.count()
    tuning_count = await Tuning_FH5.count()

    dataStatus = DataStatus(
        nation=naiton_count,
        manufacturer=manufac_count,
        car=car_count,
        decal=decal_count,
        tag=tag_count,
        tagkind=0,
        tuning=tuning_count,
    )
    return dataStatus
