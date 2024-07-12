from __future__ import annotations
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from pprint import pprint
from app.models.nation import Nation as NationDB
from app.models.manufacturer import Manufacturer as ManufacturerDB
from app.models.car import Car as CarDB
from app.models.tag import Tag as TagDB
from app.models.tag import TagKind as TagKindDB
from app.models.decal import Decal_FH5
from app.models.tuning import Tuning_FH5

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

    naiton_count = await NationDB.count()
    manufac_count = await ManufacturerDB.count()
    car_count = await CarDB.count()
    tag_count = await TagDB.count()
    decal_count = await Decal_FH5.count()
    tagkind_count = await TagKindDB.count()
    tuning_count = await Tuning_FH5.count()

    dataStatus = DataStatus(
        nation=naiton_count,
        manufacturer=manufac_count,
        car=car_count,
        decal=decal_count,
        tag=tag_count,
        tagkind=tagkind_count,
        tuning=tuning_count,
    )
    return dataStatus
