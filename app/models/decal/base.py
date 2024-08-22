"""Decal models."""

from datetime import datetime
from typing import List, Optional, Union
from beanie import Document, Link
from pydantic import Field
from app.types.http import Url
from app.models.car import Car
from app.utils.time import datetime_utc
from app.models.tag import TagItem
from pprint import pprint
from abc import abstractmethod

__all__ = ("DecalBase", "DecalName")


class DecalBase(Document):
    """DecalBase DB representation."""

    # id
    share_code: str = Field(min_length=9, max_length=9)
    car: Link[Car]
    creator: str

    imageURLs: List[Url] = Field(default=[])
    firstImage: Optional[Url]

    tags: List[Link[TagItem]] = Field(default=[])

    # backend only
    first_uploaded: datetime = Field(default_factory=datetime_utc)
    last_edited: Optional[datetime] = Field(default=None)

    @property
    def created(self) -> datetime | None:
        """Datetime car was created from ID."""
        return self.id.generation_time if self.id else None

    @abstractmethod
    def to_front(self):
        raise NotImplementedError

    class Settings:
        name = "decal"
        is_root = True
