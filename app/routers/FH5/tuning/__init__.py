from fastapi import APIRouter, Depends, Body


from app.models.FH5.tuning import Tuning as Tuning_FH5
from app.models.car import Car as CarDB
from app.models.tag import TagItem as TagDB
from app.models.FH5.car import Car_FH5

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Annotated
from app.models.FH5.components.car_details import (
    Performance,
    DetailedTunings,
    MajorParts,
    TestReadings,
)
from pprint import pprint
from bson import DBRef
import asyncio

__all__ = ("router",)

router = APIRouter(prefix="", tags=["tuning"])


class TuningCreate(BaseModel):

    shareCode: str = Field(max_length=9, min_length=9)
    car: str  # car ID
    creator: str

    tags: List[str] = Field(default=[])  # tag id list

    pi: int  # 필수
    performance: Performance  # 필수
    testReadings: TestReadings  # 필수
    tuningMajorParts: MajorParts  # 필수
    detailedTuning: Optional[DetailedTunings] = Field(default=None)  # 필수 아님


class TuningBulkCreate(BaseModel):

    car: str  # car ID
    name: str  # tuning name
    shareCode: str = Field(max_length=9, min_length=9)
    gamerTag: str
    pi: int  # 필수

    # performance: Performance  # 필수
    # testReadings: TestReadings  # 필수
    tuningMajorParts: MajorParts  # 필수
    # detailedTuning: Optional[DetailedTunings] = Field(default=None)  # 필수 아님


class TuningSearchQueryParam(BaseModel):
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=30, ge=10, le=50)


@router.get("/{carID}")
async def get_many_tunings_of_car(
    carID: str, queryParam: TuningSearchQueryParam = Depends()
):
    pprint(queryParam)
    # FIXME:
    decals = await Tuning_FH5.find_all().to_list()
    [await d.fetch_all_links() for d in decals]
    decalss = [d.to_simple_front() for d in decals]
    return decalss


@router.get("/{carID}/{tuningID}")
async def get_one_tuning(carID: str, tuningID: str):
    tuning = await Tuning_FH5.get(tuningID, fetch_links=True)

    if not tuning:
        return 200

    return await tuning.as_json()


@router.post("")
async def create_tuning(tuning: TuningCreate):
    pprint(tuning)
    # return 200

    # 1. 차 ID 확인 -> Link로 저장하기 위해서
    car = await CarDB.get(tuning.car)
    if not car:
        return

    # 2. 태그 ID 확인 -> Link로 저장하기 위해서
    # _tags = await asyncio.gather(*[TagDB.get(tagID) for tagID in tuning.tags])
    # tags = [t.to_ref() for t in _tags if t]

    # print(f"{tags=}")
    # return

    # 4. 저장
    new_tuning = Tuning_FH5(
        share_code=tuning.shareCode,
        car=car,
        creator=tuning.creator,
        # tags=tags,
        detailedTuning=tuning.detailedTuning,
        performance=tuning.performance,
        testReadings=tuning.testReadings,
        tuningMajorParts=tuning.tuningMajorParts,
        pi=tuning.pi,
    )
    # pprint(Tuning_FH5)
    await new_tuning.insert()

    return 200


@router.post("/bulk")
async def create_tuning(tunings: Annotated[List[TuningBulkCreate], Body()]):
    pprint(tunings)
    # return 200
    for tuning in tunings:

        # 1. tuning share code check
        carFH5Ref = DBRef(Tuning_FH5.get_collection_name(), tuning.car)
        tuningFH5 = await Tuning_FH5.find_one(
            Tuning_FH5.base_car_fh5 == carFH5Ref,
            Tuning_FH5.share_code == tuning.shareCode,
        )
        if tuningFH5:
            continue
        # 2. carFH5 check
        carFH5 = await Car_FH5.get(tuning.car)
        if not carFH5:
            continue

        tuningFH5 = await Tuning_FH5(
            base_car_fh5=carFH5,
            gamer_tag=tuning.gamerTag,
            name=tuning.name,
            pi=tuning.pi,
            share_code=tuning.shareCode,
            tuningMajorParts=tuning.tuningMajorParts,
            detailedTuning=None,
            testReadings=None,
            uploader="test uploader",
            performance=None,
        ).create()
        print(f"tuningFH5 : {tuningFH5.id_str}")

    return 200


@router.get("/edit")
async def get_tuning_for_edit():
    return 200


@router.delete("")
async def delete_tuning():
    return 200
