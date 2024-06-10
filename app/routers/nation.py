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
import uuid
from app.configs import awsSettings, runtimeSettings
from app.models.nation import Nation as NationDB, NationName
from beanie import WriteRules
import botocore
import urllib
from fastapi import FastAPI, File, UploadFile
import pathlib

router = APIRouter(prefix="/nation", tags=["nation"])


class NationGet(BaseModel):
    name: str
    lang: str


class NationCreate(BaseModel):

    name: List[NationName]


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

    if not nation.lang:
        return

    return 200
    nat = await NationDB.find_one(NationDB.name.lang == nation.lang, fetch_links=True)

    if nat:
        return

    # nation name i18n 먼저 저장 -> 중복이 있으면 안됨
    nationName: NationName = await NationName(
        value=nation.name, lang=nation.lang
    ).insert()

    print(f"{nationName=}")
    nationDB: NationDB = await NationDB(name=[nationName]).insert(
        link_rule=WriteRules.WRITE
    )
    print(f"{nationDB=}")
    return nationDB.model_dump(exclude=["_id", "revision_id"])


@router.post("/image")
async def add_nation(file: UploadFile):
    # TODO: 파일 업로드하고 사용 안된 임시파일 삭제하기

    # 내용 추가 중에 이미지 추가할 때 임시로 저장하는 것

    fname = pathlib.Path(file.filename)
    file_name, file_ext = fname.stem, fname.suffix

    print(f"{file.filename=}")
    random_name = uuid.uuid4()
    temp_file_name = f"{random_name}{fname.suffix}"
    base_dir = runtimeSettings.TEMPFILE_BASE_DIR
    fname_temp = pathlib.Path(base_dir, "uploads", "nation", temp_file_name).resolve()

    print(f"{fname_temp=}")

    with open(fname_temp, "wb") as f:
        nationFlag = await file.read()
        f.write(nationFlag)

    # 임시 저장한 파일 이름 다시 보내기 (어차피 경로는 POST : /nation으로 오니깐)
    return temp_file_name


@router.post("/test")
async def add_nation(file: UploadFile, name: UploadFile):
    # NationName.lang

    # nationName = nation.name[0]
    pprint(name)

    # exists = await NationDB.find_one(
    #     NationDB.name.lang == nationName.lang, NationDB.name.value == nationName.value
    # )

    # print(f"{exists=}")
    return 200

    # @router.post("/test")
    # async def add_nation(nation: NationCreate):
    #     # NationName.lang

    #     pprint(nation)
    #     nationName = nation.name[0]

    #     exists = await NationDB.find_one(
    #         NationDB.name.lang == nationName.lang, NationDB.name.value == nationName.value
    #     )

    #     print(f"{exists=}")
    #     return 200

    nat = await NationDB.find_one(NationDB.name.lang == nation.lang, fetch_links=True)

    if nat:
        return

    # nation name i18n 먼저 저장 -> 중복이 있으면 안됨
    nationName: NationName = await NationName(
        value=nation.name, lang=nation.lang
    ).insert()

    print(f"{nationName=}")
    nationDB: NationDB = await NationDB(name=[nationName]).insert(
        link_rule=WriteRules.WRITE
    )
    print(f"{nationDB=}")
    return nationDB.model_dump(exclude=["_id", "revision_id"])
