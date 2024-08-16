from __future__ import annotations
from fastapi import APIRouter, Body, Path
from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel
import asyncio

from typing import List, Dict, Any, Optional, Annotated
from pprint import pprint
from beanie import DeleteRules

from app.models.tag import TagDescription, TagName, Tag as TagDB
from app.models.tag import TagKind as TagKindDB

__all__ = ("router",)

router = APIRouter(prefix="")


class TaggingNewTags(BaseModel):
    name: str


class TaggingPostRequest(BaseModel):
    tags: List[str] = Field(default=[], description="tag id of tag already exists")
    new_tags: List[TaggingNewTags] = Field(default=[], description="new tag name")

    model_config = ConfigDict(alias_generator=to_camel)


@router.get("/1")
async def get_tagging():
    return "hello"


@router.post("/{subject_id}")
async def create_tagging(
    subject_id: Annotated[str, Path()], tags: Annotated[TaggingPostRequest, Body()]
):
    print(f"{subject_id=}")
    print()
    pprint(tags)

    for new_tag in tags.new_tags:
        tagName = await TagName.find_one(TagName.value == new_tag.name)
        if tagName:
            tagAlreadyExists = await TagDB.find_one({TagDB.name: tagName.to_ref()})
            if tagAlreadyExists:
                print("tagAlreadyExists")
                pprint(tagAlreadyExists)
        else:
            # 태그 정보 갱신 안하고 그냥 이름만 넣은 경우
            tagName = await TagDB.find_one(TagDB.initial_name == new_tag.name)
            if not tagName:
                newTag = TagDB(initial_name=new_tag.name)
                await newTag.insert()
                print("new tag added")
                pprint(newTag)
            else:
                print("tagAlreadyExists")
                pprint(tagName)

    return "hello"
