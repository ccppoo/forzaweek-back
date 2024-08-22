from __future__ import annotations
from fastapi import APIRouter
from fastapi.routing import APIRoute
from pydantic import BaseModel, Field
import asyncio

from typing import List, Dict, Any, Optional
from pprint import pprint
from beanie import DeleteRules

from app.services.image import resolve_temp_image
from app.models.tag import TagDescription, TagName, TagItem as TagDB
from app.models.tag import TagCategory as TagCategoryDB

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

    query = {"name.$id": {"$in": tag_ids}}

    tagss = await TagDB.find_many(query).to_list()
    # pprint(tagss)
    jobs2 = [t.fetch_all_links() for t in tagss]
    await asyncio.gather(*jobs2)
    return [x.to_front() for x in tagss]
