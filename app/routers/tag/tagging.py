from __future__ import annotations
from fastapi import APIRouter, Body, Path, Depends
from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel
import asyncio
from beanie.odm.fields import PydanticObjectId

from typing import List, Dict, Any, Optional, Annotated, Literal
from pprint import pprint
from beanie import DeleteRules
from app.db import mongodb

from app.models.tag import TagCategory, TagDescription, TagName, TagItem, Tagging
from app.models.user import UserAuth
from app.services.auth.deps import get_current_active_user, get_optional_active_user


__all__ = ("router",)

router = APIRouter(prefix="/tagging")

# 668e43139fea9e1931a55e8d - 블루아카이브 데칼

TAG_ID = "66c6d88405ac814a19830673"
DECAL_ID = "668e43139fea9e1931a55e8d"
TEST_USER = "66ab8776990f7c8c89d12473"


class TaggingNewTags(BaseModel):
    name: str


class TaggingTagItem(BaseModel):
    id: str


class TaggingPostRequest(BaseModel):
    tags: List[TaggingTagItem] = Field(
        default=[], description="tag id of tag already exists"
    )
    new_tags: List[TaggingNewTags] = Field(default=[], description="new tag name")

    model_config = ConfigDict(alias_generator=to_camel)


class TaggingReponse(BaseModel):
    # tags: List[TaggingReponseItem] = Field([])
    # 태그 id
    tags: List[TaggingTagItem] = Field([])


@router.get("/{post_type}/{subject_id}")
async def get_all_tags_of_subject_id(
    post_type: Annotated[str, Path()],
    subject_id: Annotated[str, Path()],
    current_user: Annotated[UserAuth, Depends(get_current_active_user)],
):
    """
    subejct_id 글에 개인이 태그 달아 놓은것 보내줌

    """
    _subject_id = PydanticObjectId(subject_id)
    current_user.user_id

    taggings = await Tagging.find(
        Tagging.subject_id == _subject_id,
        Tagging.post_type == post_type,
        {"up_vote": {"$in": [current_user.user_id]}},
    ).to_list()

    tag_ids = []

    for tagging in taggings:
        tag_ids.append({"id": str(tagging.tag.to_ref().id)})
        # pprint(tagging)

    return TaggingReponse(tags=tag_ids).model_dump()


@router.post("/{post_type}/{subject_id}")
async def do_tagging_to_subject_id(
    post_type: Annotated[str, Path()],
    subject_id: Annotated[str, Path()],
    current_user: Annotated[UserAuth, Depends(get_current_active_user)],
    tags: Annotated[TaggingPostRequest, Body()],
):
    """
    subejct_id 글에 개인이 태그 등록/업데이트 함

    1. 여기서 기존에 있는 태그는 tagging Document에 추가하고

    2. 새로 만들어진 태그는
        2-1. Tag document 새로 생성하고
        2-2. 기존 태그처럼 tagging 만들기

    3. tagging에서 혼자 태깅한 뒤 태깅을 취소할 경우
        3-1. up_vote 한 사용자가 있을 경우는 남겨둔다.
        3-2. down_vote만 있는 경우 삭제한다.
    """
    _subject_id = PydanticObjectId(subject_id)
    pprint(tags)
    print(f"{_subject_id=}")
    print(f"{current_user.user_id=}")
    # 0. 새로운 태그
    for new_tag in tags.new_tags:
        # 먼저 태그가 생성이 되었을 경우도 있으니 먼저 찾아본다.
        tagName = await TagName.find_one(TagName.value == new_tag.name)
        if tagName:
            tagAlreadyExists = await TagItem.find_one({TagItem.name: tagName.to_ref()})
            if tagAlreadyExists:
                print("tagAlreadyExists")
                pprint(tagAlreadyExists)
                tags.tags.append(TaggingTagItem(id=str(tagAlreadyExists.id)))
        else:
            # 태그 정보 갱신 안하고 그냥 이름만 넣은 경우
            tagName = await TagItem.find_one(TagItem.initial_name == new_tag.name)
            if not tagName:
                newTag = TagItem(initial_name=new_tag.name)
                await newTag.insert()
                print("new tag added")
                pprint(newTag)
                tags.tags.append(TaggingTagItem(id=str(newTag.id)))
            else:
                print("tagAlreadyExists")
                tags.tags.append(TaggingTagItem(id=str(tagName.id)))

    # 1. 기존에 했던 태그 찾기
    prev_taggings = await Tagging.find(
        Tagging.subject_id == _subject_id,
        Tagging.post_type == post_type,
        {Tagging.tagger: {"$in": [current_user.user_id]}},
    ).to_list()

    print()

    pprint(f"{prev_taggings=}")
    print()
    # return

    # 2. 기존에 있던 태그
    new_tagging_ids = {PydanticObjectId(t.id) for t in tags.tags}
    for tagging in prev_taggings:
        # 업데이트한 태그 목록 중에서 기존에 있는 태그가 없을 경우
        if not tagging.tag.to_ref().id in new_tagging_ids:
            tagging.tagger
            removeTagger = {"$pull": {"tagger": {"$eq": current_user.user_id}}}
            await tagging.update(removeTagger)
        # 태그한거 그대로 있을 경우
        else:
            # 업데이트할 거 아니니깐 빼기
            print(f"이미 tagger에 존재 : {tagging.tag.to_ref().id}")
            new_tagging_ids.remove(tagging.tag.to_ref().id)

    # 3-1. 기존에 Tagging에 존재하고, 새롭게 추가한 태그에 tagger 추가하기
    print(f"{new_tagging_ids=}")
    taggings_for_append_tagger = await Tagging.find(
        Tagging.subject_id == _subject_id,
        Tagging.post_type == post_type,
        {
            Tagging.tag.id: {
                "$in": [PydanticObjectId(tag_id) for tag_id in new_tagging_ids]
            }
        },
    ).to_list()
    print(f"기존에 있는 Tagging document 남은거, {taggings_for_append_tagger=}")
    for tagging in taggings_for_append_tagger:
        addToTagger = {"$addToSet": {Tagging.tagger: current_user.user_id}}
        await tagging.update(addToTagger)
        new_tagging_ids.remove(
            tagging.tag.to_ref().id
        )  # 기존에 있는 tagging document는 그대로 작업

    # 3-2. 기존에 없었던 Tagging인 경우 새로 만들고 추가하기
    print(f"새로 만들어야화는 Tagging document들, {new_tagging_ids=}")
    for new_tag_id in new_tagging_ids:
        _tag = await TagItem.get(new_tag_id)
        tagging = Tagging(
            subject_id=_subject_id,
            tag=_tag,
            post_type=post_type,
            up_vote=[current_user.user_id],
            tagger=[current_user.user_id],
        )
        await tagging.create()

    return


# @router.get("/{post_type}/{subject_id}/{tag_id}")
# async def get_tag_of_post_tagging(
#     post_type: Annotated[str, Path()],
#     subject_id: Annotated[str, Path()],
#     tag_id: Annotated[str, Path()],
# ):
#     """
#     게시물 태깅한 태그들 중에서 하나 가져오는 것 -> up/down vote 가져오는 거
#     """
#     _tag_id = PydanticObjectId(tag_id)
#     _subject_id = PydanticObjectId(subject_id)

#     tagging = await Tagging.find_one(
#         Tagging.subject_id == _subject_id,
#         Tagging.post_type == post_type,
#         Tagging.tag.id == _tag_id,
#     )
#     if not tagging:
#         return

#     return tagging.model_dump()


@router.post("/{post_type}/{subject_id}/{tag_id}/{vote_type}")
async def vote_tag(
    post_type: Annotated[str, Path()],
    subject_id: Annotated[str, Path()],
    tag_id: Annotated[str, Path()],
    vote_type: Annotated[Literal["up", "down"], Path()],
    user: Annotated[UserAuth, Depends(get_current_active_user)],
):
    _tag_id = PydanticObjectId(tag_id)
    _subject_id = PydanticObjectId(subject_id)

    tagging = await Tagging.find_one(
        Tagging.subject_id == _subject_id,
        Tagging.post_type == post_type,
        Tagging.tag.id == _tag_id,
    )
    if not tagging:
        return

    if vote_type == "up":
        await tagging.up_voted_from(user.user_id)
    if vote_type == "down":
        await tagging.down_voted_from(user.user_id)

    return tagging.model_dump()


@router.get("/test1")
async def test_tagging():

    tag = await TagItem.get(TAG_ID)  # 블루 아카이브
    decalID = PydanticObjectId(DECAL_ID)
    tagging = Tagging(subject_id=decalID, tag=tag, post_type="decal")
    await tagging.create()
    return tagging.model_dump()


@router.get("/test2")
async def test_tagging_up_vote():
    tag = await TagItem.get(TAG_ID)  # 블루 아카이브
    print("tag")
    pprint(tag)
    decalID = PydanticObjectId(DECAL_ID)
    works = await Tagging.find_one(Tagging.tag.id == tag.id)
    print()
    print(f"{works=}")
    tagging = await Tagging.find_one(
        Tagging.tag.id == tag.id, Tagging.subject_id == decalID
    )
    print()
    print("tagging")
    pprint(tagging)
    if not tagging:
        return

    user = await UserAuth.get(TEST_USER)
    await tagging.up_voted_from(user.user_id)

    return tagging.model_dump()


@router.get("/test3")
async def test_tagging_down_vote():
    tag = await TagItem.get(TAG_ID)  # 블루 아카이브

    decal_id = PydanticObjectId(DECAL_ID)
    tagging = await Tagging.find_one(
        Tagging.tag.id == tag.id, Tagging.subject_id == decal_id
    )

    if not tagging:
        return

    user = await UserAuth.get(TEST_USER)

    await tagging.down_voted_from(user.user_id)

    return tagging.model_dump()
