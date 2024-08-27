from fastapi import APIRouter, Query, Depends

from app.models.FH5.decal import Decal as Decal_FH5

from app.models.car import Car as CarDB
from app.models.tag import TagItem as TagDB
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Literal
from app.types.http import Url
from pprint import pprint
from bson import ObjectId
import asyncio
from app.models.FH5.decal import Decal
from app.utils.random import random_uuid
from app.services.image import resolve_temp_image

__all__ = ("router",)

router = APIRouter(prefix="/decal", tags=["decal"])


class DecalCreate(BaseModel):

    share_code: str = Field(max_length=9, min_length=9)
    car: str  # car ID
    creator: str
    imageURLs: List[str] = Field(default=[])
    firstImage: str
    tags: List[str]  # tag id list


PAGINATION_LIMIT_DEFAULT = 30
PAGINATION_ORDER_DEFAULT = "date"

TEST_USER_ID = "c786e13e-eeb8-5299-b6cc-4b9811101061"


class PaginatedRequestParam(BaseModel):
    page: Optional[int] = Query(1, description="page")
    limit: Optional[int] = Query(PAGINATION_LIMIT_DEFAULT, description="limit on page")
    order: Literal["date", "score", "replies"] = Query(
        PAGINATION_ORDER_DEFAULT, description="sort option"
    )


@router.get("")
async def get_decals(
    query: PaginatedRequestParam = Depends(),
    tags: List[str] = Query(None, description="list of tag ID"),
):
    # TODO: 여기서 조건에 맞는 데칼 보내주기
    print(f"{query=}")
    print(f"{tags=}")
    return
    decals = await Decal_FH5.find_all().to_list()
    [await d.fetch_all_links() for d in decals]
    decalss = [d.to_front() for d in decals]
    return decalss


@router.get("/test")
async def test_decal():

    decal = await Decal(
        user_id=TEST_USER_ID,
        share_code="999666333",
        gamer_tag="optims1873",
    ).create()
    return decal.model_dump()


# @router.get("/{decalID}")
# async def get_decals(decalID: str):
#     decal = await Decal_FH5.get(decalID, fetch_links=True)

#     if not decal:
#         return 200

#     return decal.to_front_read()


@router.post("")
async def create_decal(decal: DecalCreate):
    pprint(decal)
    _new_ObjectID = ObjectId()

    # 1. 차 ID 확인 -> Link로 저장하기 위해서
    car = await CarDB.get(decal.car)
    if not car:
        return
    # 2. 태그 ID 확인 -> Link로 저장하기 위해서
    _tags = await asyncio.gather(*[TagDB.get(tagID) for tagID in decal.tags])
    tags = [t.to_ref() for t in _tags if t]

    # print(f"{tags=}")
    # return

    # 3. 새로 올라온 사진 저장
    if decal.firstImage not in decal.imageURLs:
        return
    first_img_idx = decal.imageURLs.index(decal.firstImage)

    # TODO: asyncio 아니면 병렬로 수정한 후 바꿀것
    uploaded_images = []
    for img in decal.imageURLs:
        random_name = random_uuid(replace_dash="")
        httpUrl = resolve_temp_image("decal", img, random_name, str(_new_ObjectID))
        uploaded_images.append(httpUrl)

    first_image_url = uploaded_images[first_img_idx]

    print(f"{uploaded_images=}")

    # 4. 저장
    # FIXME:
    decal_FH5 = Decal_FH5(
        id=_new_ObjectID,
        share_code=decal.share_code,
        car=car,
        creator=decal.creator,
        imageURLs=uploaded_images,
        firstImage=first_image_url,
        tags=tags,
    )
    pprint(decal_FH5)
    await decal_FH5.insert()

    return 200


@router.get("/edit")
async def get_decal_for_edit():
    return 200


@router.delete("")
async def delete_decal():
    return 200
