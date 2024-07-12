"""Manufacturer models."""

from datetime import datetime
from typing import Any, List
from beanie import Document, Link
from app.models.nation import Nation
from app.models.i18n import i18n
from app.types.http import Url

__all__ = ("Manufacturer", "dbInit")


class ManufacturerName(i18n):
    # value : str
    # lang: str
    def to_front(self):
        return {"value": self.value, "lang": self.lang}


class ManufacturerDescription(i18n):
    # value : str
    # lang: str
    pass


class Manufacturer(Document):
    """Manufacturer DB representation."""

    name: List[Link[ManufacturerName]]
    name_en: str
    founded: int
    origin: Link[Nation]
    imageURL: Url

    @property
    def created(self) -> datetime | None:
        """Datetime car was created from ID."""
        return self.id.generation_time if self.id else None

    def to_json_all_lang(self, _id: bool = False) -> dict[str, Any]:
        i18ns = [x.to_front() for x in self.name]
        # 직접 id 가져오는 방법?
        _id = self.model_dump(include=["id"])["id"]

        if _id:
            return {
                "id": _id,
                "i18n": i18ns,
                "name_en": self.name_en,
                "origin": self.origin.to_json_all_lang(),
                "founded": self.founded,
                "imageURL": self.imageURL,
            }
        return {
            "i18n": i18ns,
            "name_en": self.name_en,
            "origin": self.origin,
            "founded": self.founded,
            "imageURL": self.imageURL,
        }

    def to_indexedDB(self):
        # id: string;
        # name: i18n[];
        # name_en: string;
        # founded: number;
        # nation: string; // nation ID
        # imageURL: string;
        name = {x.lang: x.value for x in self.name}
        # 직접 id 가져오는 방법?
        _id = self.model_dump(include=["id"])["id"]
        _origin_id = self.origin.model_dump(include=["id"])["id"]
        return {
            "id": _id,
            "name": name,
            "name_en": self.name_en,
            "origin": _origin_id,
            "founded": self.founded,
            "imageURL": self.imageURL,
        }

    def to_simple(self):
        _partial = self.model_dump(include=["id", "name_en", "imageURL"])
        _name = [n.to_front() for n in self.name]
        return {**_partial, "name": _name}

    class Settings:
        name = "manufacturer"
        use_state_management = True


dbInit = (ManufacturerName, ManufacturerDescription, Manufacturer)
