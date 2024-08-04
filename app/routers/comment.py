from app.models.comment import (
    TaggableComments,
    VotableComments,
    TaggableComment,
    VotableComment,
    VotableMainComment,
    CommentsBase,
    CommentBase,
)
from app.models.car import Car
from app.models.user import UserAuth
from fastapi import APIRouter, Depends, Query, Path
from typing import Annotated, Optional, Literal, List
from app.models.user.UserAuth import UserAuth
from app.services.auth.deps import get_current_active_user
from pprint import pprint
from pydantic import BaseModel, field_validator, Field
from beanie.odm.fields import PydanticObjectId

router = APIRouter(prefix="/comment")

COMMENT_SORT_OPTION = ["date", "score", "replies", "vote"]
COMMENT_LIMIT_DEFAULT = 10
COMMENT_ORDER_DEFAULT = "date"


class CommentsRequestParam(BaseModel):
    subject_id: str = Path(description="comment subjected to ")
    page: Optional[int] = Query(1, description="comment page")
    limit: Optional[int] = Query(
        COMMENT_LIMIT_DEFAULT, description="comment limit on page"
    )

    order: Literal["date", "score", "replies"] = Query(
        COMMENT_ORDER_DEFAULT, description="comment sort option"
    )


class CommentRequestParam(BaseModel):
    subject_id: str = Path(description="comment subjected to ")
    comment_id: str = Path(description="comment id")


@router.get("/{subject_id}")
async def get_comment_from_subject_id(
    options: CommentsRequestParam = Depends(),
):
    print()
    pprint(options)
    print()
    _subject_id = PydanticObjectId(options.subject_id)

    comments = await CommentsBase.find_one(
        CommentsBase.subject_to == _subject_id,
        with_children=True,
    )
    if not comments:
        return

    if comments._class_id == TaggableComments._class_id:
        comments: TaggableComments
        pass

    if comments._class_id == VotableComments._class_id:
        comments = await VotableComments.find_one(
            VotableComments.subject_to == _subject_id, fetch_links=True
        )
        if comments:
            return comments.get_id_by(page=1, limit=30, order="date")
            # return comments.to_front(page=1, limit=30, order="date") # 댓글 내용 전부 보내주는 거

    return {}


@router.get("/{subject_id}/{comment_id}")
async def get_comment_from_subject_id(
    options: CommentRequestParam = Depends(),
):
    print()
    pprint(options)
    print()
    _subject_id = PydanticObjectId(options.subject_id)
    _comment_id = PydanticObjectId(options.comment_id)

    comments = await CommentBase.find_one(
        CommentBase.id == _comment_id,
        CommentBase.subject_to == _subject_id,
        with_children=True,
    )
    if not comments:
        return

    if comments._class_id == TaggableComments._class_id:
        comments: TaggableComments
        pass

    if comments._class_id == VotableMainComment._class_id:
        comments = await VotableMainComment.get(_comment_id, fetch_links=True)
        if comments:
            return comments.to_front()  # 댓글 내용 전부 보내주는 거
            # return comments.get_id_by(page=1, limit=30, order="date")

    return {}


async def create_test_votable():
    CAR_ID = "6684cbca6b755b09a74f84fc"
    TUNING_ID = "66a1bd93c0c2a9311e907246"
    USER_ID = "66ab8776990f7c8c89d12473"

    user = await UserAuth.get(USER_ID)

    vcs = await VotableComments(subject_to=TUNING_ID, comments=[]).create()

    # subject_to
    # comments_parent
    # creator
    # value
    vmc = await VotableMainComment(
        creator=user,
        value="테스트용 일반 댓글 2",
        subject_to=TUNING_ID,
        comments_parent=str(vcs.id),
    ).create()

    # subject_to
    # comments_parent
    # creator
    # value

    vc_sub1 = await VotableComment(
        creator=user,
        value="테스트용 대댓글 4",
        subject_to=TUNING_ID,
        comments_parent=str(vcs.id),
    ).create()

    vc_sub2 = await VotableComment(
        creator=user,
        value="테스트용 대댓글 5",
        subject_to=TUNING_ID,
        comments_parent=str(vcs.id),
    ).create()

    vc_sub3 = await VotableComment(
        creator=user,
        value="테스트용 대댓글 6",
        subject_to=TUNING_ID,
        comments_parent=str(vcs.id),
    ).create()

    vmc.subComments.extend([vc_sub1, vc_sub2, vc_sub3])
    await vmc.save_changes()
    vcs.comments.append(vmc)
    await vcs.save_changes()
    return


async def create_test_taggable():
    pass


@router.post("/test/{comment_type}")
async def make_comment(comment_type: Literal["votable", "taggable"]):

    match comment_type:
        case "taggable":
            await create_test_taggable()
        case "votable":
            await create_test_votable()

    return
