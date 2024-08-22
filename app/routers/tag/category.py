from __future__ import annotations
from fastapi import APIRouter, Path, Query
from pydantic import BaseModel, Field

from typing import List, Dict, Any, Optional, Annotated, Literal
from pprint import pprint

from app.models.tag import TagDescription, TagName, TagCategory

__all__ = ("router",)

router = APIRouter(prefix="/category", tags=["tag category", "category"])


"""
66c6a30c9503900ec56fe289 - GAME
66c6a30c9503900ec56fe28c - FPS
"""


@router.get("/{tagCategoryID}")
async def get_tag_category_by_id(tagCategoryID: Annotated[str, Path()]):

    tag_cat = await TagCategory.get(tagCategoryID)
    if not tag_cat:
        return
    return await tag_cat.dump()


@router.get("/{tagCategoryID}/name")
async def get_tag_category_explaination(
    tagCategoryID: Annotated[str, Path()],
    lang: Annotated[Literal["en", "ko", "jp"], Query()] = None,
):
    """
    하나의 태그에 대해서 이름(name)에 대해서 찾는다
    """
    # print(f"{tagCategoryID=} , {lang=}")
    tag = await TagCategory.get(tagCategoryID)
    names = await tag.model_dump_name()
    return names.model_dump()


@router.get("/{tagCategoryID}/explaination")
async def get_tag_category_explaination(
    tagCategoryID: Annotated[str, Path()],
    lang: Annotated[Literal["en", "ko", "jp"], Query()] = None,
):
    """
    하나의 태그에 대해서 설명(explaination)에 대해서 찾는다
    """
    # print(f"{tagCategoryID=} , {lang=}")
    tag = await TagCategory.get(tagCategoryID)
    names = await tag.model_dump_description()
    return names.model_dump()


@router.get("/{tagCategoryID}/relation")
async def get_tag_category_relations(
    tagCategoryID: Annotated[str, Path()],
    type: Annotated[
        Literal["merged", "parent", "children", "vertical"], Query()
    ] = None,
):
    """
    하나의 태그에 대해서 병합된 태그(merged), 부모 태그(parent), 자식 태그(children)에 대해서 찾는다
    """

    # 66c6a30c9503900ec56fe291 - 헤일로
    # 66c6a73c4cd4ccf793f5fa5c - 헤일로 인피니트
    # print(f"{tagCategoryID=} {type=}")

    tag = await TagCategory.get(tagCategoryID)
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
