from __future__ import annotations
from fastapi import APIRouter
from fastapi.routing import APIRoute
from pydantic import BaseModel, Field
import asyncio

from typing import List, Dict, Any, Optional
from pprint import pprint
from beanie import DeleteRules

from app.services.image import resolve_temp_image
from app.models.tag import TagDescription, TagName, TagItem
from app.models.tag import TagCategory as TagCategoryDB
from app.utils.data.dict import remove_none

__all__ = ("router",)

router = APIRouter(prefix="/tag", tags=["tag"])


@router.get("/a")
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

    query1 = {"name.$id": {"$in": tag_ids}}
    query2 = {"_class_id": TagItem._class_id}

    tagss = await TagItem.find_many(query1, query2).to_list()
    jobs2 = [t.for_search_result(3) for t in tagss]
    jobs = await asyncio.gather(*jobs2)

    tag_keys = []
    lookup_tag_item = {}
    lookup_tag_category = {}

    tag_items = []
    for tag in jobs:
        _tag_id = tag.get("id")
        tag_keys.append(tag.get("id"))
        lookup_tag_item[_tag_id] = tag
        if m_tag := tag.get("merged_to"):
            _m_tag_id = m_tag.get("id")
            tag_keys.append(_m_tag_id)
            lookup_tag_item[_m_tag_id] = m_tag
        if p_tag := tag.get("parent"):
            _p_tag_id = p_tag["id"]
            tag_keys.append(_p_tag_id)
            lookup_tag_item[_p_tag_id] = p_tag
        if c_tag := tag.get("category"):
            _c_tag_id = c_tag["id"]
            tag_keys.append(_c_tag_id)
            lookup_tag_category[_c_tag_id] = {
                "name": c_tag.get("name"),
                "image_url": c_tag.get("image_url"),
            }

    for tag in jobs:
        _tag_item = {}
        _tag_id = tag.get("id")
        _tag_item.update(
            name=tag.get("name"),
            image_url=tag.get("image_url"),
        )
        _tag_real_item = {"id": _tag_id}
        if _m_tag := tag.get("merged_to"):
            _tag_item.update(merged_to=_m_tag.get("id"))
            _tag_real_item.update(merged_to=_m_tag.get("id"))
        if _p_tag := tag.get("parent"):
            _tag_item.update(parent=_p_tag.get("id"))
            _tag_real_item.update(parent=_p_tag.get("id"))
        if _c_tag := tag.get("category"):
            _tag_item.update(category=_c_tag.get("id"))
            _tag_real_item.update(category=_c_tag.get("id"))

        lookup_tag_item.update({_tag_id: _tag_item})

        tag_items.append(_tag_real_item)

    # Lookup -> tags, category
    data = {
        "lookup_tag": remove_none(lookup_tag_item),
        "lookup_category": remove_none(lookup_tag_category),
        "tags": tag_items,
    }
    return data


@router.get("/category")
async def search_tag_category_by_keyword(keyword: Optional[str] = None):
    print(f"{keyword=}")
    if not keyword:
        tag_cats = await TagCategoryDB.all(limit=20).to_list()
        return [await tc.as_json() for tc in tag_cats]

    tags = await TagName.find_many(
        {"value": {"$regex": f"^.*{keyword}.*$", "$options": "i"}},
    ).to_list()
    tag_ids = [t.id for t in tags]

    query1 = {"name.$id": {"$in": tag_ids}}

    tagCats = await TagCategoryDB.find_many(query1).to_list()

    return [await cat.as_json() for cat in tagCats]


@router.get("/category/id")
async def search_tag_category_by_keyword(keyword: Optional[str] = None):
    print(f"{keyword=}")
    if not keyword:
        tag_cats = await TagCategoryDB.all(limit=20).to_list()
        return [await tc.as_json() for tc in tag_cats]

    tags = await TagName.find_many(
        {"value": {"$regex": f"^.*{keyword}.*$", "$options": "i"}},
    ).to_list()
    tag_ids = [t.id for t in tags]

    query1 = {"name.$id": {"$in": tag_ids}}

    tagCats = await TagCategoryDB.find_many(query1).to_list()

    return [str(cat.id_str) for cat in tagCats]
