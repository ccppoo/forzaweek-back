from __future__ import annotations
from fastapi import APIRouter, UploadFile, File
from fastapi.websockets import WebSocketState
from pydantic import BaseModel, Field, HttpUrl, FilePath
import anyio
from typing import List, Dict, Any, Optional
import asyncio
import json
from pprint import pprint
from datetime import datetime
import uuid
from app.configs import awsSettings, runtimeSettings, cfSettings
from app.models.nation import Nation as NationDB, NationName
from beanie import WriteRules
import botocore
import urllib
from fastapi import FastAPI, File, UploadFile
import pathlib
import os
import boto3


router = APIRouter(prefix="/nation", tags=["nation"])


class NationGet(BaseModel):
    name: str
    lang: str


class NationCreate(BaseModel):

    name: List[NationName]
    name_en: str
    image: str


client_s3 = boto3.client(
    "s3",
    awsSettings.REGION,
    aws_access_key_id=awsSettings.CREDENTIALS_ACCESS_KEY,
    aws_secret_access_key=awsSettings.CREDENTIALS_SECRET_KEY,
)


client_r2 = boto3.client(
    service_name="s3",
    endpoint_url=cfSettings.R2_ENDPOINT,
    aws_access_key_id=cfSettings.ACCESS_KEY,
    aws_secret_access_key=cfSettings.SECRET_ACCESS_KEY,
    region_name=cfSettings.LOCATION,
)


@router.get("")
async def get_nation(nation: NationGet):

    nationDB = await NationDB.find_one(
        NationDB.name.value == nation.name, fetch_links=True
    )

    if nationDB:
        return nationDB.to_json(nation.lang)
        # return nationDB.model_dump(exclude=["id", "revision_id"])

    return "hello"


@router.post("")
async def add_nation(nation: NationCreate):
    # NationName.lang

    pprint(nation)

    aws_temp = "https://forzaweek-image-main-storage.s3.ap-northeast-2.amazonaws.com/{folder}/{name}"
    cf_temp = "https://fzwcdn.forzaweek.com/{folder}/{name}"
    nat = await NationDB.find_one(NationDB.name_en == nation.name_en)

    pprint(nat)

    if nat:
        # 중복됨
        return 403

    # 1. 이미지 R2로 보내기
    base_dir = runtimeSettings.TEMPFILE_BASE_DIR

    fname_temp = pathlib.Path(base_dir, "uploads", "nation", nation.image).resolve()
    if not fname_temp.exists():
        # TODO: 업로드된 이미지 다시 요청
        return 403

    # 업로드할 이미지 이름 재수정
    new_filename = f"{nation.name_en}_flag{fname_temp.suffix}"
    folder = "nation"
    new_key = f"{folder}/{new_filename}"

    client_r2.upload_file(
        Filename=fname_temp,
        Bucket=cfSettings.BUCKET,
        Key=new_key,
    )

    # 임시 파일 삭제
    os.remove(fname_temp)

    # 2. DB에 저장
    inserted_i18n = [await nname.insert() for nname in nation.name]

    nation_inserted = await NationDB(
        name=inserted_i18n,
        name_en=nation.name_en,
        imageURL=cf_temp.format(folder=folder, name=new_filename),
    ).insert()

    pprint(nation_inserted)

    return 200


@router.post("/image")
async def add_nation(file: UploadFile):
    # TODO: 파일 업로드하고 사용 안된 임시파일 삭제하기

    # 내용 추가 중에 이미지 추가할 때 임시로 저장하는 것

    fname = pathlib.Path(file.filename)
    file_name, file_ext = fname.stem, fname.suffix

    # print(f"{file.filename=}")
    random_name = uuid.uuid4()
    temp_file_name = f"{random_name}{fname.suffix}"
    base_dir = runtimeSettings.TEMPFILE_BASE_DIR
    fname_temp = pathlib.Path(base_dir, "uploads", "nation", temp_file_name).resolve()

    # print(f"{fname_temp=}")

    with open(fname_temp, "wb") as f:
        nationFlag = await file.read()
        f.write(nationFlag)

    # 임시 저장한 파일 이름 다시 보내기 (어차피 경로는 POST : /nation으로 오니깐)
    return {"image": temp_file_name}
