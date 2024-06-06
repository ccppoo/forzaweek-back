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

from app.configs import awsSettings
from app.models.nation import Nation as NationDB, NationName
from beanie import WriteRules
import botocore
import urllib


router = APIRouter(prefix="/nation", tags=["nation"])


class Nation(BaseModel):
    name: str
    lang: str


@router.get("")
async def get_nation(nation: Nation):

    nationDB = await NationDB.find_one(
        NationDB.name.value == nation.name, fetch_links=True
    )

    if nationDB:
        return nationDB.to_json(nation.lang)
        # return nationDB.model_dump(exclude=["id", "revision_id"])

    return "hello"


@router.post("")
async def add_nation(nation: Nation):
    # NationName.lang

    if not nation.lang:
        return

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
