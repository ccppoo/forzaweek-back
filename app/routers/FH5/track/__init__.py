from __future__ import annotations
from fastapi import APIRouter
from pydantic import BaseModel, Field
import asyncio
from typing import List, Dict, Any, Optional, Union
from pprint import pprint
from bson import ObjectId
from beanie import DeleteRules

from app.models.FH5.race_route import RaceRoute


from app.models.FH5.race_route.i18n import (
    RaceRouteName,
    RaceRouteDescription,
    RaceRouteNameTranslated,
)

from app.utils.random import random_uuid
from app.services.image import resolve_temp_image
from app.types import GAME

__all__ = ("router",)

router = APIRouter(prefix="/track", tags=["track"])


class FullPathImage(BaseModel):
    zoom_out: str
    zoom_in: Optional[str] = Field(
        default=None
    )  # 트랙 경로가 너무 큰 경우 한 번에 사진에 담을 수 없어서 zoom_out과 동일 할 때 사용


class TrackCreate(BaseModel):
    game: GAME = Field(default="FH5")
    category: str
    format: str
    laps: int = Field(gte=0, le=10)
    world: str
    fullPathImage: FullPathImage
    imageURLs: List[str] = Field(default=[])
    firstImage: Optional[str] = Field(default=None)
    name: List[RaceRouteName]
    name_en: str
    liberal_translation: Optional[List[RaceRouteNameTranslated]] = Field(default=None)
    tags: List[str] = Field(default=[])


@router.get("")
async def get_tracks():
    pass


@router.get("/{name_en}")
async def get_track(name_en: str):
    name_en_ = name_en.replace("_", " ")
    trackDB: Union[RaceRoute, None] = await RaceRoute.find_one(
        RaceRoute.name_en == name_en_,
        fetch_links=True,
    )

    return trackDB.to_front_read2()


@router.post("")
async def add_track(track: TrackCreate):
    pprint(track)

    trackDB: Union[RaceRoute, None] = await RaceRoute.find_one(
        RaceRoute.name_en == track.name_en,
        fetch_links=True,
    )

    # # 1. 이미 존재하는 차
    # if carDB is not None:
    #     return

    # 3-1. 새로 올라온 사진 저장 - imageURLs
    if track.imageURLs:
        if track.firstImage not in track.imageURLs:
            return
        first_img_idx = track.imageURLs.index(track.firstImage)

    # TODO: asyncio 아니면 병렬로 수정한 후 바꿀것
    uploaded_images = []
    first_image_url = None
    if track.imageURLs:
        for img in track.imageURLs:
            random_name = random_uuid(replace_dash="")
            httpUrl = resolve_temp_image(
                f"track", img, random_name, track.game, track.world
            )
            uploaded_images.append(httpUrl)

        first_image_url = uploaded_images[first_img_idx]

    # 3-2. 트랙 경로 보여주는 대표 사진 저장
    fullPath_zoom_in = track.fullPathImage.zoom_in
    track_name_ = track.name_en.replace(" ", "_")
    if fullPath_zoom_in:
        # fullPath_zi_name = f"{track.name_en.replace(' ', '_')}_zoom_in"
        fullPath_zoom_in_ = resolve_temp_image(
            f"track", fullPath_zoom_in, "zoom_in", track.game, track.world, track_name_
        )

    fullPath_zoom_out = track.fullPathImage.zoom_out
    # fullPath_zo_name = f"{track.name_en.replace(' ', '_')}_zoom_out"
    fullPath_zoom_out_ = resolve_temp_image(
        f"track", fullPath_zoom_out, "zoom_out", track.game, track.world, track_name_
    )

    # 4. 이름 저장

    _liberalTranslation = track.liberal_translation or []
    await asyncio.gather(
        *[n.insert() for n in track.name],
        *[lt.insert() for lt in _liberalTranslation],
    )

    trackDB: RaceRoute = await RaceRoute(
        imageURLs=uploaded_images,
        firstImage=first_image_url,
        name_en=track.name_en,
        name=track.name,
        category=track.category,
        format=track.format,
        fullPathImage={
            "zoom_in": fullPath_zoom_in_,
            "zoom_out": fullPath_zoom_out_,
        },
        laps=track.laps,
        game=track.game,
        tag=track.tags,
        world=track.world,
        liberal_translation=_liberalTranslation,
    ).insert()

    return trackDB.model_dump()


@router.patch("")
async def update_track():
    pass


@router.delete("/{document_id}")
async def delete_track(document_id: str):

    trackDB: Union[RaceRoute, None] = await RaceRoute.get(
        document_id,
        fetch_links=True,
    )

    if trackDB is None:
        return

    # 1. 삭제 할 것 - Link Documents
    name_delete = [tn.delete() for tn in trackDB.name]
    await asyncio.gather(*name_delete)
    if trackDB.liberal_translation:
        lt_delete = [lt.delete() for lt in trackDB.liberal_translation]
        await asyncio.gather(*lt_delete)
    # 2. 삭제 할 것 - 이미지
    # fullPathImage
    # imageURLs
    # firstImage

    # 3. 원본 문서
    await trackDB.delete()

    return
