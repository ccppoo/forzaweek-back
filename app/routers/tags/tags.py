from fastapi import APIRouter, Path, Body, Query, Depends
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Annotated, Literal
from beanie.odm.fields import PydanticObjectId

from app.models.tag import TagDescription, Tag as TagDB
from app.models.tag import TagKind as TagKindDB
from app.models.tagging import Tagging
from app.models.user import UserAuth
from app.services.auth.deps import get_current_active_user, get_optional_active_user

# from typing import TYPE_CHECKING

# if TYPE_CHECKING:
#     from app.models.user import UserAuth
from pprint import pprint

router = APIRouter(prefix="", tags=[])


class TagName(BaseModel):
    value: str
    lang: str


class TaggingItem(BaseModel):
    tag_id: str = Field(alias="tagID")
    # initial_name: str
    # name: List[TagName] = Field([])
    # imageURL: str
    up: int = Field(ge=0)
    down: int = Field(ge=0)
    up_user: List[str] = Field([])
    down_user: List[str] = Field([])


class TaggingReponse(BaseModel):
    # tags: List[TaggingReponseItem] = Field([])
    # 태그 id
    tags: List[str] = Field([])


@router.get("/{post_type}/{subject_id}")
async def get_all_tags_of_subject_id(
    post_type: Annotated[str, Path()], subject_id: Annotated[str, Path()]
):
    """
    게시물 볼 때 게시물에 달린 태그 보는 용도 (로그인 여부 X)
    """
    # subject id에 해당하는 게시물의 태그
    _subject_id = PydanticObjectId(subject_id)
    taggings = await Tagging.find_many(
        Tagging.subject_id == _subject_id, Tagging.post_type == post_type
    ).to_list()

    TaggingReponse

    tags = [str(tagging.tag.ref.id) for tagging in taggings]

    return TaggingReponse(tags=tags).model_dump()


@router.get("/{post_type}/{subject_id}/{tag_id}")
async def get_one_tag_of_subject_id(
    post_type: Annotated[str, Path()],
    subject_id: Annotated[str, Path()],
    tag_id: Annotated[str, Path()],
    current_user: Annotated[UserAuth | None, Depends(get_optional_active_user)],
):
    """
    subject_id -> tags 중에 하나의 태그
    존재하는 태그일지라도 post에 태깅을 안했을 경우 안나옴
    """
    _subject_id = PydanticObjectId(subject_id)
    _tag_id = PydanticObjectId(tag_id)

    tagging = await Tagging.find_one(
        Tagging.subject_id == _subject_id,
        Tagging.post_type == post_type,
        Tagging.tag.id == _tag_id,
        fetch_links=True,
    )

    tag: TagDB = tagging.tag
    ups = len(tagging.up_vote)
    downs = len(tagging.down_vote)

    up_user = []
    down_user = []
    if current_user:
        if current_user.user_id in tagging.up_vote:
            up_user.append(current_user.user_id)
        if current_user.user_id in tagging.down_vote:
            down_user.append(current_user.user_id)

    # name = [n.to_front() for n in tag.name]

    initial_name = tag.initial_name or tag.name[0].value
    tri = TaggingItem(
        tagID=str(tagging.tag.id),
        up=ups,
        down=downs,
        up_user=up_user,
        down_user=down_user,
        # imageURL=tag.imageURL,
        # initial_name=initial_name,
        # name=name,
    )
    return tri.model_dump()


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
    opposite = "down" if vote_type == "up" else "up"
    addToSetQuery = {"$addToSet": {f"{vote_type}_vote": user.user_id}}
    removeQuery = {"$pull": {f"{opposite}_vote": {"$eq": user.user_id}}}
    await tagging.update(addToSetQuery, removeQuery)
    await tagging.save()

    return tagging.model_dump()
