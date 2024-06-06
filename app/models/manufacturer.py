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

    def to_json(self, lang: str):
        _name = ""
        _descript = ""
        _nation = ""
        for name in self.name:
            if name.lang == lang:
                _name = name.value
                break
        for descript in self.description:
            if descript.lang == lang:
                _descript = descript.value

        for nation_name in self.origin.name:
            if nation_name.lang == lang:
                _nation = nation_name.value
        return {
            "name": _name,
            "description": _descript,
            "nation": _nation,
            "lang": lang,
        }

    class Settings:
        name = "manufacturer"


dbInit = (ManufacturerName, ManufacturerDescription, Manufacturer)
