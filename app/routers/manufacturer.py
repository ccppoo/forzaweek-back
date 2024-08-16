from __future__ import annotations
from fastapi import APIRouter, UploadFile, File
from fastapi.websockets import WebSocketState
from pydantic import BaseModel, Field
import anyio
from typing import List, Dict, Any, Optional
import asyncio
import json
from pprint import pprint
from datetime import datetime
from app.configs import awsSettings, runtimeSettings, cfSettings
from app.models.car import Car
from app.models.manufacturer import (
    Manufacturer as ManufacturerDB,
    ManufacturerName,
)
from app.models.nation import Nation as NationDB, NationName
import urllib
import boto3
import pathlib
import os
from beanie import WriteRules, DeleteRules

router = APIRouter(prefix="/manufacturer", tags=["manufacturer"])


class Nation(BaseModel):
    name: str
    locale: str


class Manufacturer(BaseModel):
    name: str
    founded: int
    description: str
    nation: str
    lang: str


class ManufacturerGet(BaseModel):
    name: str
    founded: int
    description: str
    nation: str
    lang: str


class ManufacturerEdit(BaseModel):
    id: str
    origin: str
    i18n: List[ManufacturerName]
    founded: int
    name_en: str
    imageURL: str


class ManufacturerCreate(BaseModel):
    origin: str
    i18n: List[ManufacturerName]
    founded: int
    name_en: str
    imageURL: str


client_r2 = boto3.client(
    service_name="s3",
    endpoint_url=cfSettings.R2_ENDPOINT,
    aws_access_key_id=cfSettings.ACCESS_KEY,
    aws_secret_access_key=cfSettings.SECRET_ACCESS_KEY,
    region_name=cfSettings.LOCATION,
)


@router.get("")
async def get_all_manufacturer():

    mans = await ManufacturerDB.find_all().to_list()
    [await man.fetch_all_links() for man in mans]

    a = [man.to_json_all_lang() for man in mans]
    return a


@router.post("")
async def add_manufacturer(manufacturer: ManufacturerCreate):

    cf_temp = "https://fzwcdn.forzaweek.com/{folder}/{name}"
    nat = await ManufacturerDB.find_one(ManufacturerDB.name_en == manufacturer.name_en)

    if nat:
        # 중복됨
        return 403

    #  소속 국가 확인
    origin_nation = await NationDB.get(manufacturer.origin)
    if not origin_nation:
        return 403

    # 1. 이미지 R2로 보내기
    base_dir = runtimeSettings.TEMPFILE_BASE_DIR

    fname_temp = pathlib.Path(
        base_dir, "uploads", "manufacturer", manufacturer.imageURL
    ).resolve()
    if not fname_temp.exists():
        # TODO: 업로드된 이미지 다시 요청
        return 403

    # 업로드할 이미지 이름 재수정
    new_filename = f"{manufacturer.name_en}_logo{fname_temp.suffix}"
    folder = "manufacturer"
    new_key = f"{folder}/{new_filename}"

    CONTENT_TYPE = None
    if fname_temp.suffix.endswith("svg"):
        CONTENT_TYPE = "svg+xml"
    if fname_temp.suffix.endswith("webp"):
        CONTENT_TYPE = "webp"
    if fname_temp.suffix.endswith("png"):
        CONTENT_TYPE = "png"

    client_r2.upload_file(
        Filename=fname_temp,
        Bucket=cfSettings.BUCKET,
        Key=new_key,
        ExtraArgs={"ContentType": f"image/{CONTENT_TYPE}"},
    )

    # 임시 파일 삭제
    os.remove(fname_temp)

    # 3. DB에 저장
    inserted_i18n = [await nname.insert() for nname in manufacturer.i18n]

    manufacturer_inserted = await ManufacturerDB(
        name=inserted_i18n,
        origin=origin_nation,
        name_en=manufacturer.name_en,
        founded=manufacturer.founded,
        imageURL=cf_temp.format(folder=folder, name=new_filename),
    ).insert()

    # pprint(nation_inserted)

    return 200


@router.delete("/{itemID}")
async def delete_manufacturer(itemID: str):
    manufacturer: ManufacturerDB = await ManufacturerDB.get(itemID, fetch_links=True)
    if not manufacturer:
        return

    cars = await Car.find(Car.manufacturer.id == manufacturer.to_ref().id).to_list()

    has_dependencies = len(cars)

    if has_dependencies:
        # TODO: 의존하는 제조사 DB 먼저 삭제하라고 하기
        return
    name_delete = [mn.delete() for mn in manufacturer.name]

    await asyncio.gather(*name_delete)
    await manufacturer.delete(link_rule=DeleteRules.DO_NOTHING)

    return 200


@router.post("/edit/{itemID}")
async def update_manufacturer(itemID: str, manufacturer: ManufacturerEdit):
    assert itemID == manufacturer.id

    man_old = await ManufacturerDB.get(manufacturer.id, fetch_links=True)

    NAME_EN = manufacturer.name_en
    NEW_IMAGE = not manufacturer.imageURL.startswith("https")  # blob:// ...
    man_old_origin_id = man_old.origin.model_dump(include=["id"])["id"]
    NEW_NATION = manufacturer.origin != man_old_origin_id
    print(f"{manufacturer.origin=} {man_old_origin_id=}")

    if not man_old:
        return 403

    # 1. 임시 이미지 R2로 보내기
    # NOTE: 이미지 수정 안했을 경우 기존 이미지 URL인 `https~`이므로 수정하지 않는다.
    if NEW_IMAGE:
        base_dir = runtimeSettings.TEMPFILE_BASE_DIR

        fname_temp = pathlib.Path(
            base_dir, "uploads", "manufacturer", manufacturer.imageURL
        ).resolve()
        if not fname_temp.exists():
            # TODO: 업로드된 이미지 다시 요청
            return 403

        # 업로드할 이미지 이름 재수정
        new_filename = f"{NAME_EN}_logo{fname_temp.suffix}"
        folder = "manufacturer"
        new_key = f"{folder}/{new_filename}"

        # 이전에 있던 이미지 삭제
        # nat_old.imageURL

        # 기존 버켓에 있던 이미지는 이름 그대로, 바뀜
        CONTENT_TYPE = None
        if fname_temp.suffix.endswith("svg"):
            CONTENT_TYPE = "svg+xml"
        if fname_temp.suffix.endswith("webp"):
            CONTENT_TYPE = "webp"
        if fname_temp.suffix.endswith("png"):
            CONTENT_TYPE = "png"
        client_r2.upload_file(
            Filename=fname_temp,
            Bucket=cfSettings.BUCKET,
            Key=new_key,
            ExtraArgs={"ContentType": f"image/{CONTENT_TYPE}"},
        )

        # 임시 파일 삭제
        os.remove(fname_temp)

    new_origin = None
    if NEW_NATION:
        new_origin = await NationDB.get(manufacturer.origin)

    # 이름 변경 있을 경우에만 새로 저장
    names: List[ManufacturerName] = ManufacturerName.RIGHT_JOIN(
        left=man_old.name, right=manufacturer.i18n
    )
    old_names: List[NationName] = NationName.LEFT_ONLY(
        left=man_old.name, right=manufacturer.i18n
    )

    [await n.insert() if not n.id else None for n in names]
    # 2. DB에 저장
    man_old.name = names
    man_old.name_en = NAME_EN
    if new_origin:
        man_old.origin = new_origin

    # NOTE: 이미지의 경우 이름은 그대로, 버킷에 있는 파일만 바뀌므로 업데이트 안함
    await man_old.save_changes()

    # 안쓰는 i18n 삭제
    [await name.delete() for name in old_names]

    return 200


@router.get("/edit/{itemID}")
async def get_manufacturer_for_edit(itemID: str):
    manufacturerDB = await ManufacturerDB.get(itemID, fetch_links=True)

    if not manufacturerDB:
        return

    manDB = manufacturerDB.to_json_all_lang()
    origin_id = manufacturerDB.origin.model_dump(include=["id"])["id"]
    manDB["origin"] = origin_id

    return manDB
