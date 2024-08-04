from __future__ import annotations
from datetime import datetime
from typing import Any, List, Optional, TypeVar, Generic
from beanie import Document, Link
from pydantic import BaseModel, Field
from app.types.http import Url
from .components import *
from app.utils.time import datetime_utc
from app.models.user import UserAuth
from beanie.odm.fields import PydanticObjectId

__all__ = (
    "CommentBase",
    "TaggableComment",
    "VotableComment",
    "VotableMainComment",
)


class CommentBase(Document):

    subject_to: PydanticObjectId  # comments가 속한 원본 글 (Car, tuning, decal, ... )
    comments_parent: (
        PydanticObjectId  # Comments (VotableComments, TaggableComments, 등) ID
    )

    creator: Link[UserAuth]  # 댓글 쓴 사람 UID
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
        use_state_management = True


class VotableComment(CommentBase, Votable):
    def to_front(self):
        # 반드시 fetch link 이후에 호출할 것
        # 프런트로만 보낼 것들
        # {
        #     "gamer_tag": self.creator.oauth.xbox.gamer_tag,
        #     "profile_image": self.creator.oauth.xbox.profile_image,
        # }
        data = {
            "creator": self.creator.user_id,
            "value": self.value,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
            "up_votes": len(self.up_voters),
            "down_votes": len(self.down_voters),
        }
        return data

    class Settings:
        use_state_management = True


class VotableMainComment(CommentBase, Votable, Replyable[VotableComment]):
    # 래딧처럼 일반 게시물 쓸 때 개추/비추 기능 추가하는 것
    # car, decal, track, tunning, ... 창작물 게시하는 글 말고 일반 게시물(자유게시판, 등)

    # up_voters: List[Link[UserAuth]] = Field(default=[])
    # down_voters: List[Link[UserAuth]] = Field(default=[])

    # subComments: List[Link[VotableComment]] = Field(default=[])

    def to_front(self):
        # 반드시 fetch link 이후에 호출할 것
        # 프런트로만 보낼 것들
        # {
        #     "gamer_tag": self.creator.oauth.xbox.gamer_tag,
        #     "profile_image": self.creator.oauth.xbox.profile_image,
        # }
        data = {
            "creator": self.creator.user_id,
            "value": self.value,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
            "up_votes": len(self.up_voters),
            "down_votes": len(self.down_voters),
        }
        subs = [sc.to_front() for sc in self.subComments]
        return {**data, "subComments": subs}

    async def add_subcomment(self):
        pass

    async def up_vote(self, by: Url):
        return await super().up_vote(by)

    async def down_vote(self, by: Url):
        return await super().down_vote(by)

    async def cancel_vote(self, by: Url):
        return await super().cancel_vote(by)

    class Settings:
        use_state_management = True
