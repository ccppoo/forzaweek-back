from fastapi import APIRouter, Query, Depends, Body, Path

from app.models.FH5.decal import Decal as Decal_FH5, DecalImages as DecalImages_FH5

from app.models.FH5.car import Car_FH5
from app.models.tag import TagItem as TagDB
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Literal, Annotated
from app.types.http import Url
from pprint import pprint
from bson import ObjectId, DBRef
from app.models.FH5.decal import Decal
from app.utils.random import random_uuid
from app.services.image import resolve_temp_image
from app.models.user.UserAuth import UserAuth
from app.services.auth.deps import get_current_active_user, get_optional_active_user
from app.db.query.vote import user_down_vote, user_up_vote
from beanie import Link


__all__ = ("router",)

router = APIRouter(prefix="", tags=[])


class VoteRequestParam(BaseModel):
    vote_side: Literal["up", "down"] = Path(description="vote up or down")


class DecalImageVoteParam(BaseModel):
    decal_id: str = Path(description="comment subjected to ")
    decal_image_id: str = Path(description="comment id")


class DecalImageVoteRequestParam(DecalImageVoteParam, VoteRequestParam):
    pass


@router.get("/{decal_id}/{decal_image_id}/vote")
async def fh5_decal_image_vote(
    current_user: Annotated[UserAuth | None, Depends(get_optional_active_user)],
    options: Annotated[DecalImageVoteParam, Depends()],
):
    """
    decal image vote up/down 가져오는 것
    """
    decalImages = await DecalImages_FH5.get(options.decal_image_id)
    vote_info = await decalImages.get_votes(current_user)

    return vote_info


@router.put("/{decal_id}/{decal_image_id}/vote/{vote_side}")
async def vote_decal(
    current_user: Annotated[UserAuth, Depends(get_current_active_user)],
    options: Annotated[DecalImageVoteRequestParam, Depends()],
):
    decalImages = await DecalImages_FH5.get(options.decal_image_id)
    queries = []

    print("before")
    print()
    print(decalImages.up_votes)
    print(decalImages.down_votes)

    match options.vote_side:
        case "up":
            queries = user_up_vote(current_user.user_id)
        case "down":
            queries = user_down_vote(current_user.user_id)

    await decalImages.update(queries)

    print("after")
    print()
    print(decalImages.up_votes)
    print(decalImages.down_votes)
    # vote_info = await decalImages.get_votes(current_user)
    return
