from __future__ import annotations
from fastapi import APIRouter, Body, Path
from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel
import asyncio
from beanie.odm.fields import PydanticObjectId

from typing import List, Dict, Any, Optional, Annotated
from pprint import pprint
from beanie import DeleteRules
from app.db import mongodb

from app.models.tag import TagDescription, TagName, Tag as TagDB
from app.models.tag import TagKind as TagKindDB
from app.models.tagging import Tagging
from app.models.user import UserAuth
from typing import Generic, TypeVar
from app.models.tuning import Tuning_FH5

T = TypeVar("T")

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
    """
    각 subject id가 가지고 있는 태그 정보들
    """
    return "hello"


@router.get("/test")
async def test_tagging():

    tag = await TagDB.get("668bb6d9c677bb3e3b93e651")  # 블루 아카이브
    tuningID = PydanticObjectId("66a1bd93c0c2a9311e907246")
    tagging = Tagging(subject_id=tuningID, tag=tag, post_type="tuning")
    await tagging.create()
    return tagging.model_dump()


@router.get("/test1")
async def test_tagging_up_vote():
    tag = await TagDB.get("668bb6d9c677bb3e3b93e651")  # 블루 아카이브
    print("tag")
    pprint(tag)
    tuningID = PydanticObjectId("66a1bd93c0c2a9311e907246")
    works = await Tagging.find_one(Tagging.tag.id == tag.id)
    print()
    print(f"{works=}")
    tagging = await Tagging.find_one(
        Tagging.tag.id == tag.id, Tagging.subject_id == tuningID
    )
    print()
    print("tagging")
    pprint(tagging)
    if not tagging:
        return

    # match tagging.post_type:
    #     case 'tuning':
    #         Tuning_FH5
    #         return
    user = await UserAuth.get("66ab8776990f7c8c89d12473")

    removeQuery = {"$pull": {"down_vote": {"$eq": user.user_id}}}
    addToSetQuery = {"$addToSet": {"up_vote": user.user_id}}
    await tagging.update(addToSetQuery, removeQuery)

    tagging.save()

    return tagging.model_dump()


@router.get("/test2")
async def test_tagging_down_vote():
    tag = await TagDB.get("668bb6d9c677bb3e3b93e651")  # 블루 아카이브

    tuningID = PydanticObjectId("66a1bd93c0c2a9311e907246")

    tagging = await Tagging.find_one(
        Tagging.tag.id == tag.id, Tagging.subject_id == tuningID
    )

    if not tagging:
        return

    user = await UserAuth.get("66ab8776990f7c8c89d12473")

    # addToSetQuery = {"$addToSet": {"down_vote": {"$each": [user.user_id]}}}
    removeQuery = {"$pull": {"up_vote": {"$eq": user.user_id}}}
    addToSetQuery = {"$addToSet": {"down_vote": user.user_id}}
    await tagging.update(addToSetQuery, removeQuery)

    tagging.save()

    return tagging.model_dump()


@router.post("/create/{subject_id}")
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
