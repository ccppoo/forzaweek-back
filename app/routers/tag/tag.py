from __future__ import annotations
from fastapi import APIRouter, Path, Query
from pydantic import BaseModel, Field
import asyncio

from typing import List, Dict, Any, Optional, Annotated, Literal
from pprint import pprint
from beanie import DeleteRules

from app.services.image import resolve_temp_image

from app.models.tag import TagDescription, TagName, TagItem
from app.models.tag import TagCategory

__all__ = ("router",)

router = APIRouter(prefix="/tag", tags=["tag", "tagItem"])


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


async def get_all_tags(kind: Optional[str] = None):
    # FIXME:
    return

    # a = [tag.to_front() for tag in tags]
    # return a


@router.get("/{tagID}")
async def get_tag_by_id(tagID: str):

    tag = await TagItem.get(tagID)
    return await tag.dump()


@router.get("/{tagID}/name")
async def get_tag_explaination(
    tagID: Annotated[str, Path()],
    lang: Annotated[Literal["en", "ko", "jp"], Query()] = None,
):
    """
    하나의 태그에 대해서 이름(name)에 대해서 찾는다
    """
    print(f"{tagID=} , {lang=}")
    tag = await TagItem.get(tagID)
    names = await tag.model_dump_name()
    return names.model_dump()


@router.get("/{tagID}/explaination")
async def get_tag_explaination(
    tagID: Annotated[str, Path()],
    lang: Annotated[Literal["en", "ko", "jp"], Query()] = None,
):
    """
    하나의 태그에 대해서 설명(explaination)에 대해서 찾는다
    """
    print(f"{tagID=} , {lang=}")
    tag = await TagItem.get(tagID)
    names = await tag.model_dump_description()
    return names.model_dump()


@router.get("/{tagID}/relation")
async def get_tag_relations(
    tagID: Annotated[str, Path()],
    type: Annotated[
        Literal["merged", "parent", "children", "vertical"], Query()
    ] = None,
):
    """
    하나의 태그에 대해서 병합된 태그(merged), 부모 태그(parent), 자식 태그(children)에 대해서 찾는다
    """

    # 66c6a30c9503900ec56fe291 - 헤일로
    # 66c6a73c4cd4ccf793f5fa5c - 헤일로 인피니트
    print(f"{tagID=} {type=}")

    tag = await TagItem.get(tagID)
    if not tag:
        return

    match type:
        case "merged":
            return tag.get_merge_relation()
        case "parent":
            return tag.get_parent_relation()
        case "children":
            return tag.get_children_relation()
        case "vertical":
            return tag.get_vertical_relation()
        case None:
            return tag.get_all_relations()


@router.post("/create")
async def add_tag(tag: TagCreate):

    tagDB = await TagItem.find_one(
        TagItem.name_en == tag.name_en,
        fetch_links=True,
    )

    # 1. 이미 존재하는 태그
    if tagDB:
        return

    # 2. 태그 종류 조회
    tag_kind = await TagCategoryDB.get(tag.kind)
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
    tagDB: TagItem = await TagItem(
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

    tag_old = await TagItem.get(tag.id, fetch_links=True)

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
    car: TagItem = await TagItem.get(itemID, fetch_links=True)
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
    return 200
    _tagDB = await TagItem.get(itemID, fetch_links=True)

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


@router.post("/test_create_merged")
async def create_test_tag():

    # name: List[Link[TagName]] = Field([])
    # imageURL: Optional[Url] = Field(None)  # 태그 설명하는 작은 이미지
    # description: List[Link[TagDescription]] = Field([])  # 태그 설명란
    # category: Optional[Link[TagCategory]] = Field(None)  # 태그 종류 분류
    tagname = await TagName.find_one(TagName.value == "HALO")

    if not tagname:
        return
    # TagItem.find({TagItem.name : {'$in' : []}})
    # {'name.$id': ObjectId('66c6a30c9503900ec56fe28e')}
    # {'merged_from.$id': ObjectId('66c6a73c4cd4ccf793f5fa5c')}
    haloTag = await TagItem.find_one({TagItem.name: tagname.to_ref()})
    if not haloTag:
        return
    print("병합할 목표 찾음")
    tagname = await TagName.find_one(TagName.value == "헤일로 TEST2")

    if not tagname:
        return

    # TagItem.find({TagItem.name : {'$in' : []}})
    haloInfiniteTag = await TagItem.find_one(
        {TagItem.name: tagname.to_ref()},
    )
    if not haloInfiniteTag:
        return
    print("병합될 목표 찾음")
    # await haloInfiniteTag.fetch_all_links()
    print("merge 중...")
    await TagItem.merge(haloInfiniteTag, haloTag)
    # haloTag.fetch_all_links() -> #WARNING: 무한으로 link 불러옴
    # haloTag.model_dump() -> 이거 호출하면
    print("완료")

    return haloTag.model_dump()


@router.post("/test_get_merged")
async def create_test_tag():

    # name: List[Link[TagName]] = Field([])
    # imageURL: Optional[Url] = Field(None)  # 태그 설명하는 작은 이미지
    # description: List[Link[TagDescription]] = Field([])  # 태그 설명란
    # category: Optional[Link[TagCategory]] = Field(None)  # 태그 종류 분류
    tagname = await TagName.find_one(TagName.value == "HALO")

    if not tagname:
        return
    # TagItem.find({TagItem.name : {'$in' : []}})
    haloTag = await TagItem.find_one({TagItem.name: tagname.to_ref()})
    if not haloTag:
        return

    await haloTag.fetch_all_links()
    return haloTag.model_dump()


@router.post("/test_create_blue")
async def create_test_tag():

    # name: List[Link[TagName]] = Field([])
    # imageURL: Optional[Url] = Field(None)  # 태그 설명하는 작은 이미지
    # description: List[Link[TagDescription]] = Field([])  # 태그 설명란
    # category: Optional[Link[TagCategory]] = Field(None)  # 태그 종류 분류

    cat_game = await TagCategory.get("66c6a30c9503900ec56fe289")
    if not cat_game:
        return

    tag_names = []
    tag_names.append(TagName(lang="unknown", value="블루 아카이브"))
    tag_names.append(TagName(lang="ko", value="블루 아카이브"))
    tag_names.append(TagName(lang="jp", value="ブルーアーカイブ"))
    tag_names.append(TagName(lang="en", value="Blue Archive"))
    [await tn.create() for tn in tag_names]

    # TagItem.find({TagItem.name : {'$in' : []}})
    blue_tag = await TagItem(name=tag_names, category=cat_game).create()

    return await blue_tag.dump()
