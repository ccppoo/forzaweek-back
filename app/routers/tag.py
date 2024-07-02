from __future__ import annotations
from fastapi import APIRouter
from pydantic import BaseModel, Field, validator, field_validator, root_validator
from typing import List, Dict, Any, Optional
import json
from pprint import pprint
from bson import ObjectId
from beanie import WriteRules, DeleteRules

from app.models.manufacturer import (
    Manufacturer as ManufacturerDB,
)
from app.models.nation import Nation as NationDB, NationName
from app.models.car import (
    Car as CarDB,
    CarName,
    CarShortName,
)

from app.utils.random import random_uuid
import asyncio

from app.services.image import resolve_temp_image
from app.models.tag import TagDescription, TagName, Tag as TagDB

router = APIRouter(prefix="/tag", tags=["tag"])


class TagCreate(BaseModel):

    name: List[TagName]
    name_en: str

    description: List[TagDescription]
    kind: str

    mergedTo: Optional[str] = Field(default=None)


class TagEdit(BaseModel):
    id: str

    name: List[TagName]
    name_en: str

    description: List[TagDescription]
    kind: str

    mergedTo: Optional[str] = Field(default=None)


@router.get("")
async def get_all_tags(kind: Optional[str] = None):

    tags = None
    if kind:
        tags = await TagDB.find(TagDB.kind == kind, fetch_links=True).to_list()
        pass
    if not kind:
        tags = await TagDB.find_all(fetch_links=True).to_list()

    a = [tag.to_json_all_lang() for tag in tags]
    return a


@router.post("")
async def add_tag(tag: TagCreate):

    tagDB = await TagDB.find_one(
        TagDB.name_en == tag.name_en,
        fetch_links=True,
    )

    # 1. 이미 존재하는 태그
    if tagDB:
        return

    # 2. 이름 저장
    tag_description = [td for td in tag.description if not td.is_empty()]
    tag_names = await asyncio.gather(
        *[n.insert() for n in tag.name],
    )
    tag_descriptions = await asyncio.gather(*[td.insert() for td in tag_description])

    tagDB: TagDB = await TagDB(
        name=tag_names,
        name_en=tag.name_en,
        description=tag_descriptions,
        kind=tag.kind,
    ).insert()

    return tagDB.model_dump()


@router.post("/edit/{itemID}")
async def update_tag(itemID: str, tag: TagEdit):
    assert itemID == tag.id

    tag_old = await TagDB.get(tag.id, fetch_links=True)

    if not tag_old:
        return 403

    # return
    NAME_EN = tag.name_en

    # 3. name, description
    names: List[TagName] = TagName.RIGHT_JOIN(left=tag_old.name, right=tag.name)
    old_names: List[TagName] = TagName.LEFT_ONLY(left=tag_old.name, right=tag.name)

    descriptions: List[TagDescription] = TagDescription.RIGHT_JOIN(
        left=tag_old.description, right=tag.description
    )
    old_descriptions: List[TagDescription] = TagDescription.LEFT_ONLY(
        left=tag_old.description, right=tag.description
    )

    name_jobs = [
        *[n.insert() for n in names if not n.id],
        *[n.insert() for n in descriptions if not n.id],
    ]
    # print(f"{name_jobs=}")
    if name_jobs:
        await asyncio.gather(*name_jobs)

    # 6. DB에 저장
    tag_old.name = names
    tag_old.name_en = NAME_EN
    tag_old.description = descriptions

    # NOTE: 이미지의 경우 이름은 그대로, 버킷에 있는 파일만 바뀌므로 업데이트 안함
    await tag_old.save_changes()

    # 안쓰는 i18n 삭제
    old_name_jobs = [
        *[name.delete() for name in old_names],
        *[sname.delete() for sname in old_descriptions],
    ]
    if old_name_jobs:
        await asyncio.gather(*old_name_jobs)

    return 200


@router.delete("/{itemID}")
async def delete_tag(itemID: str):
    car: TagDB = await TagDB.get(itemID, fetch_links=True)
    if not car:
        return

    name_delete = [
        *[cn.delete() for cn in car.name],
        *[cn.delete() for cn in car.short_name],
    ]
    await asyncio.gather(*name_delete)
    await car.delete(link_rule=DeleteRules.DELETE_LINKS)

    return 200


@router.get("/edit/{itemID}")
async def get_tag_for_edit(itemID: str):
    _tagDB = await TagDB.get(itemID, fetch_links=True)

    if not _tagDB:
        return

    supportLangs = ["en", "ko"]
    _lang = [desc.lang for desc in _tagDB.description if desc.lang in supportLangs]
    missingLang = [x for x in supportLangs if x not in _lang]

    tagDB = _tagDB.to_json_all_lang()

    _description = []
    if tagDB["description"]:
        _description = [*tagDB["description"]]
        _description.append([{"lang": lng, "value": ""} for lng in missingLang])
    else:
        _description = [{"lang": lng, "value": ""} for lng in missingLang]

    tagDB["description"] = _description

    return tagDB
