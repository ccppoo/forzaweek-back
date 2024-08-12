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
from app.models.board.block import BlockDataTypes

router = APIRouter(prefix="")


class PostBlockUpdate(BaseModel):
    delete: List[BlockDataTypes]


class PostEdit(Post):
    # FUTURE: 나중에 image처럼 따로 처리해야할 block data가 있을 경우 대비
    blockUpdate: PostBlockUpdate


# TODO: path 정리
@router.get("/{board_name}/{post_id}")
async def get_board_post(board_name: str, post_id: str):
    post = await Post.get(post_id)
    print(f"{board_name=} {post_id=}")
    return post


@router.get("/{post_id}")
async def get_board_post_to_edit(post_id: str):
    print()
    post = await Post.get(post_id)

    return post.model_dump()


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
    # TODO: 이미지 key path 바꾸기
    # user/upload -> board/~
    post.data.sanitize()
    post.data.remove_blank()
    post.data.update_file_key(user)  # user/upload -> board/post 로 바꾸기

    await post.save()

    return {}


@router.put("/{board_name}/{post_id}")
async def update_board_post(
    user: Annotated[UserAuth, Depends(get_current_active_user)],
    board_name: Annotated[str, Path()],
    post_id: Annotated[str, Path()],
    post: Annotated[PostEdit, Body()],
):
    # 최초 글 작성시
    print()
    print(f"{board_name=} , {post_id=}")
    # print()
    # pprint(user)
    print()
    # TODO: 이미지 key path 바꾸기
    # user/upload -> board/post
    post.data.sanitize()
    post.data.remove_blank()
    post.data.update_file_key(user)  # user/upload -> board/post 로 바꾸기

    await post.save()

    return {}
