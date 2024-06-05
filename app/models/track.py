"""Track models."""

from datetime import datetime
from typing import Annotated, Any, Optional

from beanie import Document, Link
from pydantic import BaseModel, Field
from typing import Literal, List
from .tag import Tag
from .i18n import i18n
from .track_trait import TrackType, CourseType

__all__ = ("Track", "dbInit")


class TrackName(i18n):
    # value : str
    # lang: str
    translated: str


class Track(Document):
    """Track DB representation."""

    name: TrackName
    track: TrackType
    course: CourseType
    tag: List[Link[Tag]] = Field(default=[])

    @property
    def created(self) -> datetime | None:
        """Datetime Track was added from ID."""
        return self.id.generation_time if self.id else None

    class Settings:
        name = "track"


dbInit = (Track, TrackName)
