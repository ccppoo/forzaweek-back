from __future__ import annotations
from fastapi import APIRouter, Path, Query, Body
from pydantic import BaseModel, Field, model_validator

from typing import List, Dict, Any, Optional, Annotated, Literal
from pprint import pprint

from app.models.tag import TagDescription, TagName, TagCategory

__all__ = ("router",)

router = APIRouter(prefix="/category", tags=["tag category", "category"])


class TagCategtroyCreate(BaseModel):

    imageURL: Optional[str] = Field(default=None)
    name: List[TagName]
    name_en: str

    description: List[TagDescription]
    color: str

    @model_validator(mode="before")
    @classmethod
    def model_validate(cls, data: dict) -> dict:
        names = []
        name_en = None
        for lang, value in data["name"].items():
            names.append(TagName(lang=lang, value=value))
            if lang == "en":
                name_en = value

        descriptions = []

        if decs := data.get("description"):
            for lang, value in decs.items():
                descriptions.append(TagDescription(lang=lang, value=value))

        data["name"] = names
        data["description"] = descriptions
        return {**data, "name_en": name_en}


class TagCategtroyEdit(TagCategtroyCreate):
    mergedTo: Optional[str] = Field(default=None)
    mergedFrom: Optional[List[str]] = Field(default=[])
    parent: Optional[str] = Field(default=None)
    children: Optional[List[str]] = Field(default=[])


@router.get("")
async def get_tag_categories(keyword: Annotated[str, Query()]):
    if not keyword:
        tag_cat_names = await TagName.find_many(
            {"value": {"$regex": f"^.*{keyword}.*$", "$options": "i"}},
        ).to_list()
        tag_cat_ids = [t.id for t in tag_cat_names]
        await TagCategory.find()
        return
    tag_cat = await TagCategory.all()
    if not tag_cat:
        return
    return await tag_cat.get_parents()


@router.post("")
async def create_tag_category(tagCategory: Annotated[TagCategtroyCreate, Body()]):

    pprint(tagCategory)
    [await n.create() for n in tagCategory.name]
    [await d.create() for d in tagCategory.description]
    await TagCategory(
        name=tagCategory.name,
        name_en=tagCategory.name_en,
        image_url=tagCategory.imageURL,
        description=tagCategory.description,
    ).create()

    return


@router.get("/{tagCategoryID}")
async def get_tag_category_by_id(tagCategoryID: Annotated[str, Path()]):

    if tagCategoryID.lower() == "general":
        tagcat = await TagCategory.get("66ebf118b8307ace8aa9b3bd")
        return await tagcat.as_json()

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
