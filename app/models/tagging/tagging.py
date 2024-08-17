from __future__ import annotations
from beanie import Document, Indexed, Link, BackLink
from bson.dbref import DBRef
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Optional, Literal, Set
from app.models.i18n import i18n
from app.types.http import Url

from app.models.tag import Tag
from app.models.user import UserAuth
from pprint import pprint
from beanie.odm.fields import PydanticObjectId
from datetime import datetime
from app.utils.time import datetime_utc

__all__ = ("Tagging",)


class TagReputaion(BaseModel):
    # 태그에 대해서 평가
    tag: Link[Tag]
    up_vote: List[Link[UserAuth]]
    down_vote: List[Link[UserAuth]]


class Tagging(Document):
    # id
    subject_id: PydanticObjectId  # 태깅하는 문서
    post_type: Literal["car", "decal", "track", "tuning"]
    tag: Link[Tag]
    up_vote: List[str] = Field(default=[])  # user public id
    down_vote: List[str] = Field(default=[])
    created_at: datetime = Field(default_factory=datetime_utc)

    @property
    def up_vote_count(self) -> int:
        return len(self.up_vote)

    @property
    def down_vote_count(self) -> int:
        return len(self.down_vote)

    def up_voted_from(self, user: UserAuth) -> None:
        # 이거 되는지 확인
        # { $addToSet: { tags: { $each: [ "camera", "electronics", "accessories" ] } } }
        if user in self.down_vote:
            self.down_vote.remove(user)
        self.up_vote.add(user)
        return

    def down_voted_from(self, user: UserAuth) -> None:
        self.down_vote.add(user)
        return

    def merge_from_tag(self, tagging: Tagging) -> None:
        # 태그가 병합될 경우, 중복을 제외한 상태로 업데이트
        self.up_vote.update(tagging.up_vote)
        self.down_vote.update(tagging.down_vote)

    class Settings:
        name: str = "tagging"
        use_state_management = True


dbInit = (Tagging,)
