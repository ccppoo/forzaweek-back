"""Track models."""

from datetime import datetime
from beanie import Document, Link
from pydantic import Field
from typing import List
from app.models.tag import Tag
from app.models.i18n import i18n

__all__ = ("Track", "dbInit")


class TrackName(i18n):
    # value : str
    # lang: str
    pass


class TrackLiberalTranslation(i18n):
    # value : str
    # lang: str
    pass


class TrackBase(Document):
    """Track DB representation."""

    name: List[Link[TrackName]]
    name_en: str
    liberal_translation: List[Link[TrackLiberalTranslation]]
    tag: List[Link[Tag]] = Field(default=[])
    world: str  # DLC 지역과 기본 지역 구분

    @property
    def created(self) -> datetime | None:
        """Datetime Track was added from ID."""
        return self.id.generation_time if self.id else None

    class Settings:
        name = "track"
        is_root = True
        use_state_management = True


dbInit = (TrackBase, TrackName)
