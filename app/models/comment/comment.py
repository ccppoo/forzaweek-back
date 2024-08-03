from __future__ import annotations
from datetime import datetime
from typing import Any, List, Optional
from beanie import Document, Link
from pydantic import BaseModel, Field
from app.models.i18n import i18n
from app.types.http import Url
from .components import *
from app.utils.time import datetime_utc


__all__ = (
    "CommentBase",
    "TaggableComment",
    "VotableComment",
)


class CommentBase(Document):

    creator: str  # 댓글 쓴 사람 UID
    value: str  # 댓글 내용
    created_at: datetime = Field(default_factory=datetime_utc)  # 작성 시각
    modified_at: Optional[datetime] = Field(default=None)  # 수정 시각

    class Settings:
        name = "comment"
        is_root = True
        use_state_management = True


class TaggableComment(CommentBase, Tagable):

    # tags: List[Link[Tag]] = Field(default=[])

    async def add_tag(self):
        self.tags
        return

    async def remove_tag(self):
        return

    class Settings:
        pass


class VotableComment(CommentBase, Votable):
    # 래딧처럼 일반 게시물 쓸 때 개추/비추 기능 추가하는 것
    # car, decal, track, tunning, ... 창작물 게시하는 글 말고 일반 게시물(자유게시판, 등)

    # up_voters: List[Link[UserAuth]] = Field(default=[])
    # down_voters: List[Link[UserAuth]] = Field(default=[])

    async def up_vote(self, by: Url):
        return await super().up_vote(by)

    async def down_vote(self, by: Url):
        return await super().down_vote(by)

    async def cancel_vote(self, by: Url):
        return await super().cancel_vote(by)

    class Settings:
        pass
