from __future__ import annotations
from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel, Field, HttpUrl, FilePath
from typing import List, Dict, Any, Optional
from pprint import pprint
from datetime import datetime
import uuid
from app.configs import awsSettings, runtimeSettings, cfSettings
from app.models.country import Country
from app.models.country.i18n import CountryName
from app.models.manufacturer import Manufacturer
from beanie import WriteRules, DeleteRules
from fastapi import FastAPI, File, UploadFile
import pathlib
import os
from app.cloud import client_r2
from app.services.dbState import updateDBState

router = APIRouter(prefix="/country", tags=["country"])


class CountryGet(BaseModel):
    name: str
    lang: str


class CountryCreate(BaseModel):

    i18n: List[CountryName]
    name_en: str
    imageURL: str


class CountryEdit(BaseModel):
    id: str
    i18n: List[CountryName]
    name_en: str
    imageURL: str


@router.get("")
async def get_all_country():

    countryDBs = await Country.find_all().to_list()
    [await nDB.fetch_all_links() for nDB in countryDBs]

    a = [x.to_json_all_lang() for x in countryDBs]
    return a


@router.delete("/{itemID}")
async def delete_country(itemID: str):
    country: Country = await Country.get(itemID, fetch_links=True)
    if not country:
        return
    manufacturers = await Manufacturer.find(
        Manufacturer.origin.id == country.to_ref().id
    ).to_list()
    has_dependencies = len(manufacturers)

    if has_dependencies:
        # TODO: 의존하는 제조사 DB 먼저 삭제하라고 하기
        return

    await country.delete(link_rule=DeleteRules.DELETE_LINKS)
    return 200


@router.post("")
async def add_country(country: CountryCreate):

    cf_temp = "https://fzwcdn.forzaweek.com/{folder}/{name}"
    nat = await Country.find_one(Country.name_en == country.name_en)

    if nat:
        # 중복됨
        return 403

    # 1. 이미지 R2로 보내기
    base_dir = runtimeSettings.TEMPFILE_BASE_DIR

    fname_temp = pathlib.Path(
        base_dir, "uploads", "country", country.imageURL
    ).resolve()
    if not fname_temp.exists():
        # TODO: 업로드된 이미지 다시 요청
        return 403

    # 업로드할 이미지 이름 재수정
    new_filename = f"{country.name_en}_flag{fname_temp.suffix}"
    folder = "country"
    new_key = f"{folder}/{new_filename}"

    CONTENT_TYPE = None
    if fname_temp.suffix.endswith("svg"):
        CONTENT_TYPE = "svg+xml"
    if fname_temp.suffix.endswith("webp"):
        CONTENT_TYPE = "webp"

    client_r2.upload_file(
        Filename=fname_temp,
        Bucket=cfSettings.BUCKET,
        Key=new_key,
        ExtraArgs={"ContentType": f"image/{CONTENT_TYPE}"},
    )

    # 임시 파일 삭제
    os.remove(fname_temp)

    # 2. DB에 저장
    inserted_i18n = [await nname.insert() for nname in country.i18n]

    new_country = Country(
        name=inserted_i18n,
        name_en=country.name_en,
        imageURL=cf_temp.format(folder=folder, name=new_filename),
    )
    await new_country.insert()
    await updateDBState("add", "country", "MIN", [new_country.to_ref()])

    # pprint(country_inserted)

    return 200


@router.get("/edit/{itemID}")
async def get_country_for_edit(itemID: str):
    countryDB = await Country.get(itemID, fetch_links=True)

    if not countryDB:
        return

    return countryDB.to_json_all_lang()


@router.post("/edit/{itemID}")
async def update_country(itemID: str, country: CountryEdit):
    assert itemID == country.id

    NAME_EN = country.name_en
    NEW_IMAGE = not country.imageURL.startswith("https")  # blob:// ...

    nat_old = await Country.get(country.id, fetch_links=True)

    if not nat_old:
        return 403

    # 1. 임시 이미지 R2로 보내기
    # NOTE: 이미지 수정 안했을 경우 기존 이미지 URL인 `https~`이므로 수정하지 않는다.
    if NEW_IMAGE:
        base_dir = runtimeSettings.TEMPFILE_BASE_DIR

        fname_temp = pathlib.Path(
            base_dir, "uploads", "country", country.imageURL
        ).resolve()
        if not fname_temp.exists():
            # TODO: 업로드된 이미지 다시 요청
            return 403

        # 업로드할 이미지 이름 재수정
        new_filename = f"{NAME_EN}_flag{fname_temp.suffix}"
        folder = "country"
        new_key = f"{folder}/{new_filename}"

        # 이전에 있던 이미지 삭제
        # nat_old.imageURL
        CONTENT_TYPE = None
        if fname_temp.suffix.endswith("svg"):
            CONTENT_TYPE = "svg+xml"
        if fname_temp.suffix.endswith("webp"):
            CONTENT_TYPE = "webp"
        # 기존 버켓에 있던 이미지는 이름 그대로, 바뀜
        client_r2.upload_file(
            Filename=fname_temp,
            Bucket=cfSettings.BUCKET,
            Key=new_key,
            ExtraArgs={"ContentType": f"image/{CONTENT_TYPE}"},
        )

        # 임시 파일 삭제
        os.remove(fname_temp)

    # 이름 변경 있을 경우에만 새로 저장
    names: List[CountryName] = CountryName.RIGHT_JOIN(
        left=nat_old.name, right=country.i18n
    )
    # print("새로 저장할 거")
    # print(names)
    old_names: List[CountryName] = CountryName.LEFT_ONLY(
        left=nat_old.name, right=country.i18n
    )
    # print("삭제할 거")
    # print(old_names)
    # 새로운건 저장
    [await n.insert() if not n.id else None for n in names]
    # 2. DB에 저장
    nat_old.name = names
    nat_old.name_en = NAME_EN

    # NOTE: 이미지의 경우 이름은 그대로, 버킷에 있는 파일만 바뀌므로 업데이트 안함
    await nat_old.save_changes()

    # 안쓰는 i18n 삭제
    [await name.delete() for name in old_names]

    return 200


@router.post("/image")
async def add_country_flag(file: UploadFile):
    # TODO: 파일 업로드하고 사용 안된 임시파일 삭제하기

    # 내용 추가 중에 이미지 추가할 때 임시로 저장하는 것

    fname = pathlib.Path(file.filename)
    file_name, file_ext = fname.stem, fname.suffix

    # print(f"{file.filename=}")
    random_name = uuid.uuid4()
    temp_file_name = f"{random_name}{fname.suffix}"
    base_dir = runtimeSettings.TEMPFILE_BASE_DIR
    fname_temp = pathlib.Path(base_dir, "uploads", "country", temp_file_name).resolve()

    # print(f"{fname_temp=}")

    with open(fname_temp, "wb") as f:
        countryFlag = await file.read()
        f.write(countryFlag)

    # 임시 저장한 파일 이름 다시 보내기 (어차피 경로는 POST : /country으로 오니깐)
    return {"image": temp_file_name}
