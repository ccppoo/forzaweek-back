from datetime import datetime
from typing import Any, List, Generic, TypeVar
from beanie import Document, Link
from pydantic import BaseModel, Field
from beanie.odm.fields import PydanticObjectId
from .comment import VotableSubComment, VotableMainComment
from app.utils.time import datetime_utc


__all__ = (
    "CommentsBase",
    "VotableComments",
)


class CommentsBase(Document):
    """Comments DB representation."""

    # subject_to -> 직접 ObjectID 일치하는것 검색
    subject_to: PydanticObjectId  # 댓글 달 수 있는 모델 mongodb Document ObjectId ref (car, decal, track, ... )
    created_at: datetime = Field(default_factory=datetime_utc)  # 생성일

    @property
    def created(self) -> datetime | None:
        """Datetime car was created from ID."""
        return self.id.generation_time if self.id else None

    class Settings:
        name = "comments"
        is_root = True
        use_state_management = True


class VotableComments(CommentsBase):
    comments: List[Link[VotableMainComment]] = Field(default=[])

    # 이런거 등등
    async def sorted_by_up_vote():
        pass

    def to_front(self, page: int, limit: int, order: str):
        # 반드시 fetch link 이후에 호출할 것
        comments_parsed = [c.to_front() for c in self.comments]
        return comments_parsed

    def get_id_by(self, page: int, limit: int, order: str):
        # 조건에 만족하는 댓글 ID 프런트로 보내는 것
        comment_ids = [str(c.id) for c in self.comments]
        # TODO: 쿼리 조건에 만족하는 document ID 보내기
        return {"comments": comment_ids}

    class Settings:
        use_state_management = True
