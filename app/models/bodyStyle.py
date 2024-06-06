"""Nation models."""

from datetime import datetime
from typing import Annotated, Any, Optional

from beanie import Document, Indexed, Link
from pydantic import BaseModel, EmailStr, Field
from typing import Literal, List
import pymongo
from .i18n import i18n


__all__ = ("BodyStyle", "dbInit")


class BodyStyleName(i18n):
    # value : str
    # lang: str
    pass


class BodyStyle(Document):
    """Nation DB representation."""

    name: List[Link[BodyStyleName]]

    @property
    def created(self) -> datetime | None:
        """Datetime car was created from ID."""
        return self.id.generation_time if self.id else None

    def to_json(self, lang: str):
        for na in self.name:
            if na.lang == lang:
                return {"name": na.value}

    def get_value(self, lang: str):
        for na in self.name:
            if na.lang == lang:
                return na.value

    class Settings:
        name = "bodyStyle"


dbInit = (BodyStyle, BodyStyleName)
