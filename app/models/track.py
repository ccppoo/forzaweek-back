"""Track models."""

from datetime import datetime
from typing import Annotated, Any, Optional

from beanie import Document, Link
from pydantic import BaseModel, Field
from typing import Literal, List
import pymongo
from .car import Car
from .car_stat import CarStat
from .tag import Tag, TrackTag
from .i18n import i18n, Locale

__all__ = ("Track",)


class Track(Document):
    """Track DB representation."""

    name: i18n
    type: i18n
    course_type: i18n
    tag: List[Link[TrackTag]] = Field(default=[])

    @property
    def created(self) -> datetime | None:
        """Datetime Track was added from ID."""
        return self.id.generation_time if self.id else None

    class Settings:
        name = "track"
