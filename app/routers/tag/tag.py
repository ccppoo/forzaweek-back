from __future__ import annotations
from fastapi import APIRouter
from pydantic import BaseModel, Field
import asyncio

from typing import List, Dict, Any, Optional
from pprint import pprint
from beanie import DeleteRules

from app.services.image import resolve_temp_image
from app.models.tag import TagDescription, TagName, Tag as TagDB
from app.models.tag import TagKind as TagKindDB

__all__ = ("router",)

router = APIRouter(prefix="")


class TagCreate(BaseModel):

    imageURL: Optional[str] = Field(default=None)
    name: List[TagName]
    name_en: str

    description: List[TagDescription]
    kind: str

    mergedTo: Optional[str] = Field(default=None)


class TagEdit(BaseModel):
    id: str
    imageURL: Optional[str] = Field(default=None)

    name: List[TagName]
    name_en: str

    description: List[TagDescription]
    kind: str

    # management
    parentTag: Optional[str] = Field(default=None)
    childrenTag: List[str] = Field(default=[])
    mergedTo: Optional[str] = Field(default=None)
    mergedFrom: List[str] = Field(default=[])


@router.get("/all")
async def get_all_tags(kind: Optional[str] = None):

    tags = None
    if kind:
        tags = await TagDB.find(TagDB.kind == kind, fetch_links=True).to_list()
        pass
    if not kind:
        tags = await TagDB.find_all(fetch_links=True).to_list()

    a = [tag.to_front() for tag in tags]
    return a


@router.get("/{tagID}")
async def get_tag_by_id(tagID: str, kind: Optional[str] = None):

    tag = await TagDB.get(tagID, fetch_links=True)

    return tag.to_front_simple()


@router.get("/search/a")
async def search_tag_by_keyword(keyword: Optional[str] = None):
    """
    TODO:
    태그 검색할 때 자동완성으로 보여주는 태그 목록들
    프론트에서 500ms 딜레이로 요청을 보내지만 딜레이나 백엔드에서 제어 및 캐싱 전략 짤 것
    """
    print(f"{keyword=}")

    tags = await TagName.find_many(
        {"value": {"$regex": f"^.*{keyword}.*$", "$options": "i"}},
    ).to_list()

    tag_ids = [t.id for t in tags]
    # print(f"{tag_ids=}")

    query = {"name.$id": {"$in": tag_ids}}

    tagss = await TagDB.find_many(query).to_list()
    # pprint(tagss)
    jobs2 = [t.fetch_all_links() for t in tagss]
    await asyncio.gather(*jobs2)
    return [x.to_front() for x in tagss]


@router.post("/create")
async def add_tag(tag: TagCreate):

    tagDB = await TagDB.find_one(
        TagDB.name_en == tag.name_en,
        fetch_links=True,
    )

    # 1. 이미 존재하는 태그
    if tagDB:
        return

    # 2. 태그 종류 조회
    tag_kind = await TagKindDB.get(tag.kind)
    if not tag_kind:
        return

    # 3. 사진
    imageHttpUrl = None
    if tag.imageURL:
        tagKindImageName = f"tag_kind_{tag.name_en}_icon"
        imageHttpUrl = resolve_temp_image(
            "tagkind", tag.imageURL, tagKindImageName, tag.name_en
        )

    # 4. 이름 저장
    tag_description = [td for td in tag.description if not td.is_empty()]
    tag_names = await asyncio.gather(
        *[n.insert() for n in tag.name],
    )
    tag_descriptions = await asyncio.gather(*[td.insert() for td in tag_description])

    # 당장 ㄴㄴ
    # parent
    # children
    # mergedTo
    # mergedFrom
    tagDB: TagDB = await TagDB(
        name=tag_names,
        name_en=tag.name_en,
        description=tag_descriptions,
        imageURL=imageHttpUrl,
        kind=tag_kind,
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
