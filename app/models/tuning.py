"""Tuning models."""

from datetime import datetime
from typing import Annotated, Any, Optional

from beanie import Document, Link
from pydantic import BaseModel, EmailStr, Field
from typing import Literal, List
import pymongo
from .car import Car
from .car_stat import CarStat
from .tag import Tag

__all__ = ("Tuning",)


class Tuning(Document):
    """Tuning DB representation."""

    car: Link[Car]
    creator: str
    share_code: str = Field(min_length=9, max_length=9)
    stat: CarStat
    tags: List[Link[Tag]] = Field(default=[])

    @property
    def created(self) -> datetime | None:
        """Datetime tuning was created from ID."""
        return self.id.generation_time if self.id else None

    class Settings:
        name = "tuning"
