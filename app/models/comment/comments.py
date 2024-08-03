from datetime import datetime
from typing import Any, List, Generic, TypeVar
from beanie import Document, Link
from pydantic import BaseModel, Field
from beanie.odm.fields import PydanticObjectId
from .comment import VotableComment, TaggableComment
from app.utils.time import datetime_utc


__all__ = (
    "CommentsBase",
    "VotableComments",
    "TaggableComments",
)

T = TypeVar("T")


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
    comments: List[Link[VotableComment]] = Field(default=[])

    # 이런거 등등
    async def sorted_by_up_vote():
        pass

    class Settings:
        pass


class TaggableComments(CommentsBase):
    comments: List[Link[TaggableComment]] = Field(default=[])

    class Settings:
        pass
