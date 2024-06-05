"""Manufacturer models."""

from datetime import datetime
from typing import Annotated, Any, Optional

from beanie import Document, Indexed, Link
from .nation import Nation
from pydantic import BaseModel, EmailStr, Field
from typing import Literal, List
import pymongo
from .i18n import i18n


__all__ = ("Manufacturer", "dbInit")


class ManufacturerName(i18n):
    # value : str
    # lang: str
    pass


class ManufacturerDescription(i18n):
    # value : str
    # lang: str
    pass


class Manufacturer(Document):
    """Manufacturer DB representation."""

    name: List[Link[ManufacturerName]]
    founded: int
    description: List[Link[ManufacturerDescription]]
    origin: Link[Nation]

    @property
    def created(self) -> datetime | None:
        """Datetime car was created from ID."""
        return self.id.generation_time if self.id else None

    class Settings:
        name = "manufacturer"


dbInit = (ManufacturerName, ManufacturerDescription, Manufacturer)
