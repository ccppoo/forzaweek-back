from __future__ import annotations
from beanie import Document, Indexed, Link
from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Set, Annotated
from app.models.i18n import i18n
from app.types.http import Url

from app.models.tag import TagItem
from app.models.user import UserAuth
from pprint import pprint
from beanie.odm.fields import PydanticObjectId
from datetime import datetime
from app.utils.time import datetime_utc
import pymongo
from .query import TaggingQuery

__all__ = ("Tagging",)


class Tagging(Document):
    """
    tagging은 사용자 각자 개인이 가지고 있는 것이 아니라

    [Post + Tag] <- 태그에 추가한 사람 목록 list에 추가

    하는 형식으로 저장된다.

    각자 개인이 어떤 게시물에 어떤 Tagging을 했는지 확인하기 위해서는 쿼리를 다시 해야한다.
    """

    # id
    subject_id: Annotated[PydanticObjectId, Indexed()]  # 태깅하는 문서
    post_type: Annotated[
        Literal["car", "decal", "track", "tuning"], Indexed(index_type=pymongo.TEXT)
    ]
    tag: Annotated[Link[TagItem], Indexed()]
    up_votes: List[str] = Field(default=[])  # user public id
    down_votes: List[str] = Field(default=[])  # user public id
    tagger: List[str] = Field(default=[])  # user public id
    created_at: datetime = Field(default_factory=datetime_utc)

    @property
    def up_vote_count(self) -> int:
        return len(self.up_votes)

    @property
    def down_vote_count(self) -> int:
        return len(self.down_votes)

    async def up_voted_from(self, user_id: str) -> None:
        queries = TaggingQuery.up_vote_user(user_id)
        await self.update(*queries)
        await self.save_changes()
        return

    async def down_voted_from(self, user_id: str) -> None:
        queries = TaggingQuery.down_vote_user(user_id)
        await self.update(*queries)
        await self.save_changes()
        return

    def merge_from_tag(self, tagging: Tagging) -> None:
        # 태그가 병합될 경우, 중복을 제외한 상태로 업데이트
        self.up_votes.update(tagging.up_votes)
        self.down_votes.update(tagging.down_votes)

    class Settings:
        name: str = "tagging"
        use_state_management = True
