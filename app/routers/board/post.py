from app.models.user import UserAuth
from app.models.tag import Tag
from fastapi import APIRouter, Depends, Query, Path, Body
from typing import Annotated, Optional, Literal, List
from app.models.user.UserAuth import UserAuth
from app.services.auth.deps import get_current_active_user, get_optional_active_user
from pprint import pprint
from pydantic import BaseModel, field_validator, Field
from beanie.odm.fields import PydanticObjectId
from app.models.board import Post

router = APIRouter(prefix="")


@router.get("/{board_name}/{post_id}")
async def get_board_post(board_name: str, post_id: str):
    post = await Post.get(post_id)
    print(f"{board_name=} {post_id=}")
    return post


@router.post("/{board_name}")
async def create_board_post(
    user: Annotated[UserAuth, Depends(get_current_active_user)],
    board_name: Annotated[str, Path()],
    post: Annotated[Post, Body()],
):
    # 최초 글 작성시
    print()
    print(f"{board_name=}")
    print()
    pprint(user)
    print()
    post.data.sanitize()
    post.data.remove_blank()
    await post.save()

    return {}
