from app.models.comment import (
    TaggableComments,
    VotableComments,
    TaggableComment,
    VotableComment,
)
from app.models.car import Car
from fastapi import APIRouter, Depends
from typing import Annotated
from app.models.user.UserAuth import UserAuth
from app.services.auth.deps import get_current_active_user
from pprint import pprint

router = APIRouter(prefix="/comment")


@router.post("/temp")
async def make_comment():

    Comments = TaggableComments[Car]

    subject = "asdasd"
    comments = await Comments(
        subject_to=subject,
    ).create()

    comment = await TaggableComment(
        creator="temp creator", value="테스트 댓글"
    ).create()
    return


@router.post("/subcomment")
async def make_subcomment():
    Comments = TaggableComments[Car]

    Comment = TaggableComment

    subject = "asdasd"
    coment = await Comment.get("66ae27fda5ad2bb4fa259371")

    comment2 = await Comment(creator="temp creator222", value="테스트 댓글222").create()

    coment.subComments.append(comment2)
    await coment.save_changes()

    comments = await Comments.get("66ae27fda5ad2bb4fa259370")
    comments.comments.append(coment)
    await comments.save_changes()
    return


@router.get("/subs")
async def get_subcomments():
    Comments = TaggableComments[Car]
    Comment = TaggableComment

    comment = await Comment.get("66ae27fda5ad2bb4fa259371", fetch_links=True)
    for x in comment.subComments:
        pprint(x.model_dump())
    try:
        return comment.model_dump()
    except:
        pass
    return
