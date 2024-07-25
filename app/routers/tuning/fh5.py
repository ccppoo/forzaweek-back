from fastapi import APIRouter, Depends

from app.models.tuning import Tuning_FH5
from app.models.car import Car as CarDB
from app.models.tag import Tag as TagDB

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from app.models.stat.fh5 import Performance, DetailedTunings, MajorParts, TestReadings
from pprint import pprint
import asyncio

__all__ = ("tuningRouter",)

tuningRouter = APIRouter(prefix="/tuning", tags=["tuning"])


class TuningCreate(BaseModel):

    share_code: str = Field(max_length=9, min_length=9)
    car: str  # car ID
    creator: str

    tags: List[str] = Field(default=[])  # tag id list

    pi: int  # 필수
    performance: Performance  # 필수
    testReadings: TestReadings  # 필수
    tuningMajorParts: MajorParts  # 필수
    detailedTuning: Optional[DetailedTunings] = Field(default=None)  # 필수 아님


class TuningSearchQueryParam(BaseModel):
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=30, ge=10, le=50)


@tuningRouter.get("/{carID}")
async def get_many_tunings_of_car(
    carID: str, queryParam: TuningSearchQueryParam = Depends()
):
    pprint(queryParam)
    decals = await Tuning_FH5.find_all().to_list()
    [await d.fetch_all_links() for d in decals]
    decalss = [d.to_simple_front() for d in decals]
    return decalss


@tuningRouter.get("/{carID}/{tuningID}")
async def get_one_tuning(carID: str, tuningID: str):
    tuning = await Tuning_FH5.get(tuningID, fetch_links=True)

    if not tuning:
        return 200

    return tuning.to_simple_front()


@tuningRouter.post("")
async def create_tuning(tuning: TuningCreate):
    pprint(tuning)
    # return 200

    # 1. 차 ID 확인 -> Link로 저장하기 위해서
    car = await CarDB.get(tuning.car)
    if not car:
        return

    # 2. 태그 ID 확인 -> Link로 저장하기 위해서
    _tags = await asyncio.gather(*[TagDB.get(tagID) for tagID in tuning.tags])
    tags = [t.to_ref() for t in _tags if t]

    # print(f"{tags=}")
    # return

    # 4. 저장
    new_tuning = Tuning_FH5(
        share_code=tuning.share_code,
        car=car,
        creator=tuning.creator,
        tags=tags,
        detailedTuning=tuning.detailedTuning,
        performance=tuning.performance,
        testReadings=tuning.testReadings,
        tuningMajorParts=tuning.tuningMajorParts,
        pi=tuning.pi,
    )
    # pprint(Tuning_FH5)
    await new_tuning.insert()

    return 200


@tuningRouter.get("/edit")
async def get_tuning_for_edit():
    return 200


@tuningRouter.delete("")
async def delete_tuning():
    return 200
