"""Decal models."""

from datetime import datetime
from typing import List, Optional
from beanie import Document, Link
from pydantic import Field
from app.types.http import Url
from app.models.car import Car
from app.utils.time import datetime_utc
from app.models.tag import Tag
from pprint import pprint

__all__ = ("DecalBase", "DecalName")


class DecalBase(Document):
    """DecalBase DB representation."""

    # id
    share_code: str
    car: Link[Car]
    creator: str

    images: List[Url]
    firstImage: Optional[Url]

    tags: List[Link[Tag]]

    # backend only
    created: datetime = Field(default_factory=datetime_utc)

    @property
    def created(self) -> datetime | None:
        """Datetime car was created from ID."""
        return self.id.generation_time if self.id else None

    class Settings:
        name = "decal"
        is_root = True
        use_state_management = True
