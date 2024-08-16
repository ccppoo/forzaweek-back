from app.models.comment import (
    TaggableComments,
    VotableComments,
    TaggableComment,
    VotableSubComment,
    VotableMainComment,
    CommentsBase,
    CommentBase,
)
from app.models.user import UserAuth
from app.models.tag import Tag
from fastapi import APIRouter, Depends, Query, Path
from typing import Annotated, Optional, Literal, List
from app.models.user.UserAuth import UserAuth
from app.services.auth.deps import get_current_active_user, get_optional_active_user
from pprint import pprint
from pydantic import BaseModel, field_validator, Field
from beanie.odm.fields import PydanticObjectId

__all__ = ("router",)

router = APIRouter(prefix="")

COMMENT_SORT_OPTION = ["date", "score", "replies", "vote"]
COMMENT_LIMIT_DEFAULT = 10
COMMENT_ORDER_DEFAULT = "date"


class CommentsRequestParam(BaseModel):
    subject_id: str = Path(description="comment subjected to ")


class CommentsPaginatedRequestParam(CommentsRequestParam):
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


class SubCommentRequestParam(BaseModel):
    subject_id: str = Path(description="comment subjected to ")
    comment_id: str = Path(description="comment id")
    sub_comment_id: str = Path(description="sub-comment id")


class CommentVoteRequestParam(BaseModel):
    subject_id: str = Path(description="comment subjected to ")
    comment_id: str = Path(description="comment id")
    vote: Literal["up", "down"] = Query(description="vote up or down")


class SubCommentVoteRequestParam(CommentVoteRequestParam):

    sub_comment_id: str = Path()


@router.get("/{subject_id}")
async def get_comment_from_subject_id(
    options: CommentsPaginatedRequestParam = Depends(),
):
    # print()
    # pprint(options)
    # print()
    _subject_id = PydanticObjectId(options.subject_id)

    comments = await CommentsBase.find_one(
        CommentsBase.subject_to == _subject_id, with_children=True
    )
    # subComment -> 여기서 children _class_id 참조해서 알아서 캐스팅해서 가져옴, 따로 get 할 필요 없음

    # pprint(comments)
    if not comments:
        return

    if comments._class_id == TaggableComments._class_id:
        return comments.get_id_by(page=1, limit=30, order="date")

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
    current_user: Annotated[UserAuth | None, Depends(get_optional_active_user)],
    options: CommentRequestParam = Depends(),
):
    _subject_id = PydanticObjectId(options.subject_id)
    _comment_id = PydanticObjectId(options.comment_id)

    comments = await CommentBase.find_one(
        CommentBase.id == _comment_id,
        CommentBase.subject_to == _subject_id,
        with_children=True,
    )
    # subComment -> 여기서 children _class_id 참조해서 알아서 캐스팅해서 가져옴, 따로 get 할 필요 없음

    if not comments:
        return

    if comments._class_id == TaggableComment._class_id:
        comments: TaggableComment
        await comments.fetch_all_links()
        return comments.to_front()

    if comments._class_id == VotableMainComment._class_id:
        comments = await VotableMainComment.get(_comment_id, fetch_links=False)
        await comments.fetch_link("creator")
        if comments:
            cmts = comments.to_front(current_user)
            return cmts  # 댓글 내용 전부 보내주는 거
            # return comments.model_dump()
            # return comments.get_id_by(page=1, limit=30, order="date")

    return {}


@router.patch("/{subject_id}/{comment_id}/vote")
async def vote_comment_from_subject_id(
    current_user: Annotated[UserAuth, Depends(get_current_active_user)],
    options: Annotated[CommentVoteRequestParam, Depends()],
):
    _subject_id = PydanticObjectId(options.subject_id)
    _comment_id = PydanticObjectId(options.comment_id)

    comments = await CommentBase.find_one(
        CommentBase.id == _comment_id,
        CommentBase.subject_to == _subject_id,
        with_children=True,
    )
    # subComment -> 여기서 children _class_id 참조해서 알아서 캐스팅해서 가져옴, 따로 get 할 필요 없음

    if not comments:
        return

    if comments._class_id == VotableMainComment._class_id:
        comments = await VotableMainComment.get(_comment_id, fetch_links=False)
        if options.vote == "up":
            await comments.up_vote(current_user.user_id)
        if options.vote == "down":
            await comments.down_vote(current_user.user_id)
    return


@router.get("/{subject_id}/{comment_id}/{sub_comment_id}")
async def get_sub_comment_from_comment(
    current_user: Annotated[UserAuth | None, Depends(get_optional_active_user)],
    options: SubCommentRequestParam = Depends(),
):
    # print()
    # pprint(options)
    # print()
    _subject_id = PydanticObjectId(options.subject_id)
    _comment_id = PydanticObjectId(options.comment_id)
    _sub_comment_id = PydanticObjectId(options.sub_comment_id)

    subComment = await CommentBase.find_one(
        CommentBase.id == _sub_comment_id,
        CommentBase.parent == _comment_id,
        CommentBase.subject_to == _subject_id,
        with_children=True,
        fetch_links=True,
    )
    # subComment -> 여기서 children _class_id 참조해서 알아서 캐스팅해서 가져옴, 따로 get 할 필요 없음
    # pprint(subComment)
    if not subComment:
        return

    if subComment._class_id == TaggableComments._class_id:
        # subComment: TaggableComments
        pass

    if subComment._class_id == VotableSubComment._class_id:
        return subComment.to_front(current_user)

    return {}


@router.patch("/{subject_id}/{comment_id}/{sub_comment_id}/vote")
async def vote_sub_comment_from_comment(
    current_user: Annotated[UserAuth, Depends(get_current_active_user)],
    options: Annotated[SubCommentVoteRequestParam, Depends()],
):
    _subject_id = PydanticObjectId(options.subject_id)
    _comment_id = PydanticObjectId(options.comment_id)
    _sub_comment_id = PydanticObjectId(options.sub_comment_id)

    subComment = await CommentBase.find_one(
        CommentBase.id == _sub_comment_id,
        CommentBase.parent == _comment_id,
        CommentBase.subject_to == _subject_id,
        with_children=True,
        fetch_links=True,
    )
    # subComment -> 여기서 children _class_id 참조해서 알아서 캐스팅해서 가져옴, 따로 get 할 필요 없음

    if not subComment:
        return

    if subComment._class_id == VotableSubComment._class_id:
        # subComment = await VotableSubComment.get(_sub_comment_id, fetch_links=False)
        if options.vote == "up":
            await subComment.up_vote(current_user.user_id)
        if options.vote == "down":
            await subComment.down_vote(current_user.user_id)

    return


@router.post("/{subject_id}")
async def create_comment(options: Annotated[CommentsRequestParam, Depends()]):
    pass


@router.patch("/{subject_id}/{comment_id}")
async def modify_comment(
    current_user: Annotated[UserAuth, Depends(get_current_active_user)],
    options: Annotated[CommentRequestParam, Depends()],
):
    pass


@router.delete("/{subject_id}/{comment_id}")
async def delete_comment(
    current_user: Annotated[UserAuth, Depends(get_current_active_user)],
    options: Annotated[CommentRequestParam, Depends()],
):
    pass


@router.post("/{subject_id}/{comment_id}")
async def create_sub_comment(
    current_user: Annotated[UserAuth, Depends(get_current_active_user)],
    options: Annotated[CommentRequestParam, Depends()],
):
    pass


@router.patch("/{subject_id}/{comment_id}/{sub_comment_id}")
async def modify_sub_comment(
    current_user: Annotated[UserAuth, Depends(get_current_active_user)],
    options: Annotated[SubCommentRequestParam, Depends()],
):
    pass


@router.delete("/{subject_id}/{comment_id}/{sub_comment_id}")
async def delete_sub_comment(
    current_user: Annotated[UserAuth, Depends(get_current_active_user)],
    options: Annotated[SubCommentRequestParam, Depends()],
):
    pass


async def create_test_votable(subject_id: str):
    CAR_ID = "6684cbca6b755b09a74f84fc"
    SUBJECT_ID = subject_id
    USER_ID = "66ab8776990f7c8c89d12473"

    user = await UserAuth.get(USER_ID)

    vcs = await VotableComments(
        subject_to=PydanticObjectId(SUBJECT_ID), comments=[]
    ).create()

    vmc = await VotableMainComment(
        creator=user,
        value="테스트용 일반 댓글 2",
        subject_to=SUBJECT_ID,
        parent=str(vcs.id),
    ).create()

    vc_sub1 = await VotableSubComment(
        creator=user,
        value="테스트용 대댓글 4",
        subject_to=SUBJECT_ID,
        parent=str(vmc.id),
    ).create()

    vc_sub2 = await VotableSubComment(
        creator=user,
        value="테스트용 대댓글 5",
        subject_to=SUBJECT_ID,
        parent=str(vmc.id),
    ).create()

    vc_sub3 = await VotableSubComment(
        creator=user,
        value="테스트용 대댓글 6",
        subject_to=SUBJECT_ID,
        parent=str(vmc.id),
    ).create()

    vmc.subComments.extend([vc_sub1, vc_sub2, vc_sub3])
    # vmc.subComments.extend([vc_sub1])
    await vmc.save_changes()
    vcs.comments.append(vmc)
    await vcs.save_changes()
    return


async def create_test_taggable(subject_id: str):
    CAR_ID = "6684cbca6b755b09a74f84fc"
    DECAL_ID = "668e43139fea9e1931a55e8d"
    SUBJECT_ID = PydanticObjectId(subject_id)
    USER_ID = "66ab8776990f7c8c89d12473"

    user = await UserAuth.get(USER_ID)

    tcs = await TaggableComments(subject_to=SUBJECT_ID, comments=[]).create()

    tags = []
    decal_tag_1 = await Tag.get("668bb6d9c677bb3e3b93e651")
    tc = await TaggableComment(
        creator=user,
        value="테스트용 태그 댓글 1",
        subject_to=SUBJECT_ID,
        parent=str(tcs.id),
        tags=[decal_tag_1],
    ).create()

    tcs.comments.append(tc)
    await tcs.save_changes()

    return


@router.post("/test/{comment_type}")
async def make_comment(
    comment_type: Literal["votable", "taggable"],
    subject: Annotated[str | None, Query()],
):

    match comment_type:
        case "taggable":
            TUNING_ID = "66a1bd93c0c2a9311e907246"
            if subject:
                await create_test_taggable(subject)
        case "votable":
            if subject:
                await create_test_votable(subject)

    return


@router.post("/vote/test")
async def make_comment():
    vmc = await VotableMainComment.get("66b03dc0ff8e20f2f84de0e1")
    user = await UserAuth.get("66ab8776990f7c8c89d12473")
    vmc.up_voters.append(user.user_id)
    await vmc.save_changes()
    return
