from fastapi import APIRouter, Query, Depends, Body

from app.models.FH5.decal import Decal as Decal_FH5, DecalImages as DecalImages_FH5

from app.models.FH5.car import Car_FH5
from app.models.tag import TagItem as TagDB
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Literal, Annotated
from app.types.http import Url
from pprint import pprint
from bson import ObjectId, DBRef
import asyncio
from app.models.FH5.decal import Decal
from app.utils.random import random_uuid
from app.services.image import resolve_temp_image
from app.models.user.UserAuth import UserAuth
from app.services.auth.deps import get_current_active_user, get_optional_active_user

from app.services.image.file_key import promote_to_permanent
from beanie import Link


__all__ = ("router",)

router = APIRouter(prefix="", tags=["decal"])


class DecalCreate(BaseModel):

    car: Link[Car_FH5]  # car ID
    share_code: str = Field(max_length=9, min_length=9, alias="shareCode")
    gamer_tag: str = Field(alias="gamerTag")
    image_urls: List[str] = Field(default=[], alias="imageURLs")


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


@router.get("/{decalID}")
async def get_decals(decalID: str):
    # TODO: 여기서 조건에 맞는 데칼 보내주기
    print(f"{decalID=}")
    decal = await Decal_FH5.get(decalID)

    return await decal.as_json()
    # return decal.model_dump()


@router.get("/{decalID}/image")
async def get_decal_image_ids(
    decalID: str,
    current_user: Annotated[UserAuth | None, Depends(get_optional_active_user)],
):
    # TODO: 여기서 조건에 맞는 데칼 보내주기
    print(f"{decalID=}")
    decalDBRef = DBRef(Decal_FH5.get_collection_name(), ObjectId(decalID))
    decalImages = await DecalImages_FH5.find(
        DecalImages_FH5.decalBase == decalDBRef
    ).to_list()
    return [decalImage.id_str for decalImage in decalImages]


@router.get("/{decalID}/image/{decalImageID}")
async def get_decal_images(
    decalID: str,
    decalImageID: str,
    current_user: Annotated[UserAuth | None, Depends(get_optional_active_user)],
):
    # TODO: 여기서 조건에 맞는 데칼 보내주기
    print(f"{decalID=}")
    decalDBRef = DBRef(Decal_FH5.get_collection_name(), ObjectId(decalID))
    decalImages = await DecalImages_FH5.get(decalImageID)
    return await decalImages.to_front()
    # return [await decalImage.to_front(current_user) for decalImage in decalImages]


@router.post("")
async def upload_decal(
    decal: Annotated[DecalCreate, Body()],
    current_user: Annotated[UserAuth, Depends(get_current_active_user)],
):
    # carFH5
    # share_code
    # gamer_tag
    # uploader
    pprint(decal)

    decalFH5 = await Decal_FH5(
        base_car_FH5=decal.car,
        share_code=decal.share_code,
        gamer_tag=decal.gamer_tag,
        uploader=current_user,
    ).create()

    print("promoting urls")
    destination = "FH5/decal"
    promoted_urls = [
        await promote_to_permanent(image_url, destination, current_user)
        for image_url in decal.image_urls
    ]

    print("Creating Decal Images ")

    decalImages_FH5 = await DecalImages_FH5(
        uploader=current_user, decalBase=decalFH5, images=promoted_urls
    ).create()

    return 200


@router.get("/edit")
async def get_decal_for_edit():
    return 200


@router.delete("")
async def delete_decal():
    return 200
