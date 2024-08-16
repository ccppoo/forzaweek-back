from __future__ import annotations
from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import json
from pprint import pprint
from beanie import DeleteRules

import asyncio

from app.services.image import resolve_temp_image
from app.models.tag import TagKindName, TagKindDescription, TagKind as TagKindDB

router = APIRouter(prefix="/tagkind", tags=["tagkind"])


class TagKindCreate(BaseModel):

    imageURL: Optional[str] = Field(default=None)

    name: List[TagKindName]
    name_en: str

    description: List[TagKindDescription]


class TagKindEdit(BaseModel):
    id: str

    imageURL: Optional[str]

    name: List[TagKindName]
    name_en: str

    description: List[TagKindDescription]


@router.get("")
async def get_all_tagKinds(kind: Optional[str] = None):

    tagKinds = await TagKindDB.find_all(fetch_links=True).to_list()

    a = [tagKind.to_front() for tagKind in tagKinds]
    return a


@router.post("")
async def add_tagKind(tagKind: TagKindCreate):

    tagKindDB = await TagKindDB.find_one(
        TagKindDB.name_en == tagKind.name_en,
        fetch_links=True,
    )

    # 1. 이미 존재하는 태그
    if tagKindDB:
        return

    # 2. 사진
    imageHttpUrl = None
    if tagKind.imageURL:
        tagKindImageName = f"tag_kind_{tagKind.name_en}_icon"
        imageHttpUrl = resolve_temp_image(
            "tagkind", tagKind.imageURL, tagKindImageName, tagKind.name_en
        )

    # 2. 이름 저장
    tagKind_description = [td for td in tagKind.description if not td.is_empty()]
    tagKind_names = await asyncio.gather(
        *[n.insert() for n in tagKind.name],
    )
    tag_descriptions = await asyncio.gather(
        *[td.insert() for td in tagKind_description]
    )

    tagKindDB: TagKindDB = await TagKindDB(
        imageURL=imageHttpUrl,
        name=tagKind_names,
        name_en=tagKind.name_en,
        description=tag_descriptions,
    ).insert()

    return tagKindDB.model_dump()


@router.post("/edit/{itemID}")
async def update_tagKind(itemID: str, tag: TagKindEdit):
    assert itemID == tag.id

    tag_old = await TagKindDB.get(tag.id, fetch_links=True)

    if not tag_old:
        return 403

    # return
    NAME_EN = tag.name_en

    # 3. name, description
    names: List[TagKindName] = TagKindName.RIGHT_JOIN(left=tag_old.name, right=tag.name)
    old_names: List[TagKindName] = TagKindName.LEFT_ONLY(
        left=tag_old.name, right=tag.name
    )

    descriptions: List[TagKindDescription] = TagKindDescription.RIGHT_JOIN(
        left=tag_old.description, right=tag.description
    )
    old_descriptions: List[TagKindDescription] = TagKindDescription.LEFT_ONLY(
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
async def delete_tagKind(itemID: str):
    tagKind: TagKindDB = await TagKindDB.get(itemID, fetch_links=True)
    if not tagKind:
        return

    # name_delete = [
    #     *[tkn.delete() for tkn in tagKind.name],
    #     *[tkd.delete() for tkd in tagKind.description],
    # ]
    await tagKind.delete(link_rule=DeleteRules.DELETE_LINKS)
    # await asyncio.gather(*name_delete)

    return 200


@router.get("/edit/{itemID}")
async def get_tag_for_edit(itemID: str):
    _tagKindDB = await TagKindDB.get(itemID, fetch_links=True)

    if not _tagKindDB:
        return

    supportLangs = ["en", "ko"]
    _lang = [desc.lang for desc in _tagKindDB.description if desc.lang in supportLangs]
    missingLang = [x for x in supportLangs if x not in _lang]

    tagKindDB = _tagKindDB.to_front()

    if missingLang:
        _description = []
        # 일부만 없을 경우
        if tagKindDB["description"]:
            _description = [*tagKindDB["description"]]
            _description.append([{"lang": lng, "value": ""} for lng in missingLang])
        # 전부 없을 경우
        else:
            _description = [{"lang": lng, "value": ""} for lng in missingLang]
        tagKindDB["description"] = _description

    return tagKindDB
